function [im] = load_FPA_data(fp,camera,wavelength,angle)
%LOAD_FPA_DATA this loads the image data\

if wavelength > 9999
    fn = strcat(fp,'spectral__CAM',num2str(camera),'_fpaTeempCorr_degC_',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
else
    fn = strcat(fp,'spectral__CAM',num2str(camera),'_fpaTeempCorr_degC_',num2str(wavelength),'nm_angle',num2str(angle),'deg.tiff');
    end

%load image data
im = imread(fn);
end