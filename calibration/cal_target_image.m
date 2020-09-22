% figure;
% hold on
% plot(mean(center_CAM1(ii,110:170)))
% end
% hold off

 im1center = h5read('center.hdf5','/image1');
 im2center = h5read('center.hdf5','/image2');
 
 im1left = h5read('left.hdf5','/image1');
 im2left = h5read('left.hdf5','/image2');
 
 im1right = h5read('right.hdf5','/image1');
 im2right = h5read('right.hdf5','/image2');
 
 im1cold = h5read('cold.hdf5','/image1');
 im2cold = h5read('cold.hdf5','/image2');
 

 subplot(3,2,1); 
 imagesc(im1center-im1cold)
 colorbar
 caxis([0,1000])
 
 subplot(3,2,3);
 imagesc(im1left-im1cold)
 colorbar
 caxis([0,1000])
 
 subplot(3,2,5);
 imagesc(im1right-im1cold)
 colorbar
 caxis([0,1000])
 
  subplot(3,2,2); 
 imagesc(im2center-im2cold)
 colorbar
 %caxis([0,1000])
 
 subplot(3,2,4);
 imagesc(im2left-im2cold)
 colorbar
 %caxis([0,1000])
 
 subplot(3,2,6);
 imagesc(im2right-im2cold)
 colorbar
 %caxis([0,1000])