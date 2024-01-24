# *optiflow*

## Usage

- To track a single pixel on the screen
```
python track.py --item pixel --camera 0
```

- To select a zone on the screen
```
python track.py --item zone --camera 0
```

- To select a zone and draw a rough mesh
```
python track.py --item zone --camera 0 --mesh
```

## Variations

- Switch to an external webcam
```
python track.py --item zone --camera 1 --mesh
```