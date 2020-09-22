function [im] = dead_pixel_corr(im)
%DEAD_PIXEL_CORR replaces dead pixels with median value

upper = 60000;
lower = 5000;

med = mean2(im);

im(im>upper) = med;
im(im<lower) = med;
end

