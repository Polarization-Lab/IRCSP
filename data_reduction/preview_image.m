function [] = preview_image(wavelength,angle)
%This fn will show a preview of an image 
%   wavelength is the wavelength 
%   angle is the angle of the LP
if wavelength > 9999
    fn1 = strcat('spectral_1_CAM1__',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
    fn2 = strcat('spectral_1_CAM2__',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
else
    fn1 = strcat('spectral_1_CAM1__0',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
    fn2 = strcat('spectral_1_CAM2__0',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
end

%load image data
im1 = imread(fn1);
im2 = imread(fn2);

%load FPA temp data

%plot images
subplot(1,2,1),imshow(histeq(im1),hot(65536));
title('Camera 1')
colorbar
subplot(1,2,2),imshow(histeq(im2),hot(65536));
title('Camera 2')
colorbar
%subplot(2,2,3),imhist(im1,6e4);
%subplot(2,2,4),imhist(im2,6e4);

end

