# *optiflow*

## Usage

### 1 - To track a single pixel on the screen
```
python main.py --item pixel
```

### 2 - To select a zone on the screen
```
python main.py --item zone
```

### 3 - To select a zone and draw a rough mesh
```
python main.py --item zone --mesh
```

### 4 - To select a zone and track it
```
python main.py --item poi
```

### 5 - To observe the limits of the optical flow
```
python main.py --item limits --folder [FOLDER_NAME] --add
```

## Variations

- Switch to an external webcam
```
python main.py --item poi --camera 1
```