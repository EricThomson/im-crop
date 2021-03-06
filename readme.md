# im-crop
Simple module to crop out rectangles from a larger image and save subimage. For building up
training data for CNNs when you have very large images. Work in progress. There is
one module where you can control the size (`im_cropper.py`) and one that sets images to a fixed
size (`im_cropper_fixed_size.py`).

## Set up environment and clone repo
If using conda:

    conda create --name crop
    conda activate crop
    conda install opencv=4
    conda install numpy

Get the files: go to directory where you want repo and at your conda prompt:    

    git clone https://github.com/EricThomson/im-crop.git

And it should work.

## Usage
Briefly, run the image cropper module, draw rectangle with right mouse click, click **s** to save rectangle.
For fixed size, double right click to draw rectangle.

More details: this is not plug and play yet: in the file, you will need to change base_path
to the path that contains the large images you want to crop. Change output_path to the
path where you want to save the smaller cropped pngs. Then set the image_ind, the index
of the image path you want to crop.

You will see a largish image (you can set window_params to change size, position of window).

Use mouse to set a square region. It will be highlighted in white and show you the height/width
when you release the mouse. If you want to save that rectangular region, just click the letter
`s` on your keyboard.

Press esc to exit the window. To move to next image, change the image_ind manually.

## To do
- Have option of cycling through all images in input folder.
- Add gui using pyqt to let user select image or file. Make it more like labelimg.
- Set image type as parameter rather than fixed.
