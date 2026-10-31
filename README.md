# IntrAA-SD

# Dataset Train-Test Split

This repository contains the code to get the **training** and **testing** images of the dataset.

## Requirements

* Python 3.8 or later

## Project Structure

```text
.
├── dataset/
```

## Usage

Run the following command:

```bash
python split_script.py --input_dir /path/to/dataset_expanded --output_dir /path/to/desired_output 
```

## Output

After execution, the output directory will contain separate folders for:

* Training images
* Testing images
