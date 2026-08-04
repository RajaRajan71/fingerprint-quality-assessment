import os
import glob
from tabulate import tabulate
from quality_assessment import quality_gate

def run_tests():
    image_dir = "test_images/"
    image_paths = glob.glob(os.path.join(image_dir, "*.*"))
    
    if not image_paths:
        print(f"No test images found in {image_dir}! Please add 20 sample images.")
        return

    table_data = []

    for path in sorted(image_paths):
        filename = os.path.basename(path)
        res = quality_gate(path)
        
        status = "✅ PASS" if res["passed"] else "❌ REJECT"
        
        table_data.append([
            filename,
            status,
            res["composite_score"],
            res["blur"]["blur_score"],
            res["brightness"]["brightness"],
            f"{res['glare']['glare_fraction']*100:.1f}%",
            f"{res['roi']['roi_fraction']*100:.1f}%",
            res["ridge"]["ridge_score"]
        ])

    headers = ["Filename", "Status", "Score", "Blur", "Brightness", "Glare", "ROI %", "Ridge Score"]
    print("\n=================== QUALITY GATE EVALUATION REPORT ===================")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    run_tests()