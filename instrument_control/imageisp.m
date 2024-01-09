im1 = h5read('center924_8.hdf5','/image1');
im1pol = h5read('right924_8.hdf5','/image1');
im1dark = h5read('dark_low1.hdf5','/image1');
im2 = h5read('center924_8.hdf5','/image2');
im2pol = h5read('right924_8.hdf5','/image2');
im2dark = h5read('dark_low1.hdf5','/image2');


%% set plotting ranges

c1r= [5.22*10^4,5.29*10^4];
c2r =[2.5*10^4,2.9*10^4];

 subplot(3,2,1);
 imagesc(im1)
 colorbar
 caxis(c1r)
 title('Camera 1, Unpolarized')
 
 
 subplot(3,2,2);
 imagesc(im2)
 colorbar
 caxis(c2r)
  title('Camera 2, Unpolarized')
  
  subplot(3,2,3);
 imagesc(im1pol)
 colorbar
 caxis(c1r)
 title('Camera 1,Polarized')

 
 subplot(3,2,4);
 imagesc(im2pol)
 colorbar
 caxis(c2r)
  title('Camera 2, Polarized')
  
 subplot(3,2,5);
 imagesc(im1dark)
 colorbar
 caxis(c1r)
 title('Camera 1, Darkfield')

 
 subplot(3,2,6);
 imagesc(im2dark)
 colorbar
 caxis(c2r)
  title('Camera 2, Darkfield')
  

