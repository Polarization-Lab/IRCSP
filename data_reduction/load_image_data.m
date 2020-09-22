function [im] = load_image_data(fp,camera,wavelength,angle)
%LOAD_IMAGE_DATA this loads the image data\

if wavelength > 9999
    fn = strcat(fp,'spectral_1_CAM',num2str(camera),'__',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
else
    fn = strcat(fp,'spectral_1_CAM',num2str(camera),'__',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
end

%load image data
im = imread(fn);

%replace dead pixels
im = dead_pixel_corr(im);

end

