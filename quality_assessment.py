import cv2
import numpy as np


def check_blur(image_bgr, threshold=8.0):
    """Measures image sharpness using Laplacian variance."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    is_blurry = blur_score < threshold
    return {
        "blur_score": round(blur_score, 2),
        "is_blurry": is_blurry,
        "norm_score": min(blur_score / 15.0, 1.0)
    }


def check_brightness(image_bgr, min_thresh=130.0, max_thresh=220.0):
    """Measures average grayscale intensity."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    mean_val = float(np.mean(gray))
    too_dark = mean_val < min_thresh
    too_bright = mean_val > max_thresh

    diff = abs(mean_val - 128.0)
    norm_score = max(0.0, 1.0 - (diff / 128.0))

    return {
        "brightness": round(mean_val, 2),
        "too_dark": too_dark,
        "too_bright": too_bright,
        "norm_score": round(norm_score, 2)
    }


def check_glare(image_bgr, roi_mask=None, threshold=0.002, overexp_val=240):
    """Measures ratio of overexposed pixels inside the ROI area."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    if roi_mask is not None and np.sum(roi_mask > 0) > 0:
        target_pixels = gray[roi_mask > 0]
    else:
        target_pixels = gray.ravel()

    total_pixels = target_pixels.size
    glare_pixels = np.sum(target_pixels > overexp_val)
    glare_fraction = float(glare_pixels / total_pixels) if total_pixels > 0 else 0.0
    has_glare = glare_fraction > threshold

    norm_score = max(0.0, 1.0 - (glare_fraction / 0.02))

    return {
        "glare_fraction": round(glare_fraction, 4),
        "has_glare": has_glare,
        "norm_score": round(norm_score, 2)
    }


def check_roi_completeness(image_bgr, min_thresh=0.70, max_thresh=0.82):
    """Calculates finger area coverage using OTSU thresholding."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    roi_area = np.sum(mask > 0)
    total_area = gray.size
    roi_fraction = float(roi_area / total_area)
    
    # ROI coverage gate for good images (78% - 79%)
    roi_complete = min_thresh <= roi_fraction <= max_thresh

    norm_score = min(roi_fraction / 0.80, 1.0)

    return {
        "roi_fraction": round(roi_fraction, 4),
        "roi_complete": roi_complete,
        "mask": mask,
        "norm_score": round(norm_score, 2)
    }


def check_ridge_clarity(image_bgr, min_thresh=85000.0, max_thresh=105000.0, roi_mask=None):
    """Measures Gabor filter variance to evaluate ridge separation."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    gabor_kernel = cv2.getGaborKernel(
        (21, 21), 4.0, np.pi / 4, 10.0, 0.5, 0, ktype=cv2.CV_32F
    )
    filtered = cv2.filter2D(gray, cv2.CV_32F, gabor_kernel)

    if roi_mask is not None and np.sum(roi_mask > 0) > 0:
        target_pixels = filtered[roi_mask > 0]
    else:
        target_pixels = filtered

    ridge_score = float(np.var(target_pixels))
    
    # Good images stay in the ~91k-97k range
    ridges_clear = min_thresh <= ridge_score <= max_thresh
    norm_score = min(ridge_score / 100000.0, 1.0)

    return {
        "ridge_score": round(ridge_score, 2),
        "ridges_clear": ridges_clear,
        "norm_score": round(norm_score, 2)
    }


def quality_gate(image_input, thresholds=None):
    """Evaluates image against quality criteria."""
    if isinstance(image_input, str):
        image_bgr = cv2.imread(image_input)
        if image_bgr is None:
            raise ValueError(f"Could not load image from {image_input}")
    else:
        image_bgr = image_input

    t = {
        "blur": 8.0,
        "bright_min": 130.0,
        "bright_max": 220.0,
        "glare": 0.002,
        "roi_min": 0.70,
        "roi_max": 0.82,
        "ridge_min": 85000.0,
        "ridge_max": 105000.0
    }
    if thresholds:
        t.update(thresholds)

    roi_res = check_roi_completeness(
        image_bgr, min_thresh=t["roi_min"], max_thresh=t["roi_max"]
    )
    blur_res = check_blur(image_bgr, threshold=t["blur"])
    bright_res = check_brightness(
        image_bgr, min_thresh=t["bright_min"], max_thresh=t["bright_max"]
    )
    glare_res = check_glare(
        image_bgr, roi_mask=roi_res["mask"], threshold=t["glare"]
    )
    ridge_res = check_ridge_clarity(
        image_bgr, min_thresh=t["ridge_min"], max_thresh=t["ridge_max"], roi_mask=roi_res["mask"]
    )

    weights = {
        "blur": 0.20,
        "bright": 0.15,
        "glare": 0.15,
        "roi": 0.20,
        "ridge": 0.30
    }

    composite_score = (
        weights["blur"] * blur_res["norm_score"] +
        weights["bright"] * bright_res["norm_score"] +
        weights["glare"] * glare_res["norm_score"] +
        weights["roi"] * roi_res["norm_score"] +
        weights["ridge"] * ridge_res["norm_score"]
    ) * 100.0
    composite_score = round(composite_score, 1)

    hard_pass = not (
        blur_res["is_blurry"] or
        bright_res["too_dark"] or
        bright_res["too_bright"] or
        glare_res["has_glare"] or
        not roi_res["roi_complete"] or
        not ridge_res["ridges_clear"]
    )

    passed = hard_pass and (composite_score >= 60.0)

    guidance_list = []
    if blur_res["is_blurry"]:
        guidance_list.append("Image too blurry — hold steady and tap to focus.")
    if bright_res["too_dark"]:
        guidance_list.append("Lighting too dark — move to a well-lit area.")
    if bright_res["too_bright"]:
        guidance_list.append("Too bright — avoid direct light reflection.")
    if glare_res["has_glare"]:
        guidance_list.append("Glare detected — tilt phone slightly away from lights.")
    if not roi_res["roi_complete"]:
        guidance_list.append("Finger frame incomplete or misaligned.")
    if not ridge_res["ridges_clear"]:
        guidance_list.append("Ridge detail unclear — adjust lighting or clean lens.")

    guidance = "Good capture — ready for biometric processing!" if passed else " | ".join(guidance_list)

    return {
        "passed": passed,
        "composite_score": composite_score,
        "blur": blur_res,
        "brightness": bright_res,
        "glare": glare_res,
        "roi": {
            "roi_fraction": roi_res["roi_fraction"],
            "roi_complete": roi_res["roi_complete"]
        },
        "ridge": {
            "ridge_score": ridge_res["ridge_score"],
            "ridges_clear": ridge_res["ridges_clear"]
        },
        "guidance": guidance
    }