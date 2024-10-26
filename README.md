# How to Run `main.py`

## Step 1: Prerequisites
1. Install Python 3.8.  
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
   
## Step 2: Download Data  
Download `im.mat` from [https://osf.io/k4cyq](https://osf.io/k4cyq) and place it in the same directory as `main.py`.

## Step 3: First-Time Setup  
1. Open `main.py` and modify the first line:
 ```python
   db = Database(img_source, trial_num=3, load_imgs=True)
  ```
2. Run the script:
```bash
  python main.py
```
3. After the first run, set `load_imgs` back to `False`:
```python
  db = Database(img_source, trial_num=3, load_imgs=False)
```
## Step 4: Run the Script
To run the script in future:
```bash
python main.py
```



