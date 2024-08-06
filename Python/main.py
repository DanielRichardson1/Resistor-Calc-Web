from resistorCalculations import getResistance
from roboflow import Roboflow
from IPython.display import Image, clear_output

clear_output()
rf = Roboflow(api_key="YOUR API KEY", model_format="yolov5")


# main
def main():
    print(getResistance(['brown', 'black', 'orange']))


if __name__ == '__main__':
    main()
