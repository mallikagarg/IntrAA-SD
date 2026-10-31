import argparse
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split

def main():
    parser = argparse.ArgumentParser(description="Split a dataset of file pairs into train and test sets.")
    parser.add_argument("--input_dir", type=str, required=True, help="Path to the original dataset directory.")
    parser.add_argument("--output_dir", type=str, required=True, help="Path where the train and test folders will be created.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for splitting (default: 42).")
    parser.add_argument("--test_size", type=float, default=0.2, help="Proportion of the dataset to include in the test split (default: 0.2).")
    
    args = parser.parse_args()

    source_dir = Path(args.input_dir)
    output_base_dir = Path(args.output_dir)
    
    train_dir = output_base_dir / "train"
    test_dir = output_base_dir / "test"

    all_samples = []
    labels = []

    if not source_dir.exists():
        print(f"Error: Input directory '{source_dir}' does not exist.")
        return

    for class_dir in source_dir.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name
            stems = set(f.stem for f in class_dir.iterdir() if f.is_file())
            for stem in stems:
                all_samples.append((class_name, stem, class_dir))
                labels.append(class_name)

    if not all_samples:
        print(f"No files found in {source_dir}. Please check your directory structure.")
        return

    print(f"Found {len(all_samples)} unique sample pairs across {len(set(labels))} classes.")

    train_idx, test_idx = train_test_split(
        range(len(all_samples)), 
        test_size=args.test_size,
        stratify=labels, 
        random_state=args.seed
    )

    def copy_files(indices, target_base_dir):
        for idx in indices:
            class_name, stem, class_dir = all_samples[idx]
            
            dest_dir = target_base_dir / class_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            for file_path in class_dir.glob(f"{stem}.*"):
                dest_path = dest_dir / file_path.name
                shutil.copy2(file_path, dest_path)

    print(f"Copying {len(train_idx)} samples (files + JSONs) to the training set...")
    copy_files(train_idx, train_dir)

    print(f"Copying {len(test_idx)} samples (files + JSONs) to the test set...")
    copy_files(test_idx, test_dir)

    print(f"Dataset split complete! Output saved to: {output_base_dir.absolute()}")

if __name__ == "__main__":
    main()