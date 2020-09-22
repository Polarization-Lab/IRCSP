function [] = preview_image(fp,wavelength,angle)
%This fn will show a preview of an image 
%   wavelength is the wavelength 
%   angle is the angle of the LP
if wavelength > 9999
    fn1 = strcat(fp,'spectral_1_CAM1__',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
    fn2 = strcat(fp,'spectral_1_CAM2__',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
else
    fn1 = strcat(fp,'spectral_1_CAM1__0',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
    fn2 = strcat(fp,'spectral_1_CAM2__0',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
end

%load image data
im1 = imread(fn1);
im2 = imread(fn2);

%dead pixel correction
im1 = dead_pixel_corr(im1);
im2 = dead_pixel_corr(im2);

%find max and min data information
max1 = mean(max(im1));
max2 = mean(max(im2)) ;

min1 = mean(min(im1));
min2 = mean(min(im2)) ;

edges1 = linspace(min1,max1,100);
edges2 = linspace(min2,max2,100);
%set histogram binning arrays

%plot images
sgtitle(strcat(' \lambda = ',num2str(wavelength/1000) ,' \mum, AOLP = ',num2str(angle), '^\circ'));
subplot(2,2,1),imshow(histeq(im1));
title('Camera 1')
colorbar
subplot(2,2,2),imshow(histeq(im2));
title('Camera 2')
colorbar
h1=subplot(2,2,3);
histogram(im1,'BinEdges',edges1);
ylim(h1, [0,1e4]);
h2 = subplot(2,2,4);
histogram(im2,'BinEdges',edges2);
ylim(h2,[0,1e4]);

end

