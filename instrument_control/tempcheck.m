t1 = h5read('darklong2.hdf5','/temp1');
images = h5read('darklong2.hdf5','/image1');
%t1 = [t1;  h5read('darklong2.hdf5','/temp1')];

snr= zeros(50);
%images= images(120:140,130:140,:);
for i = [1 50]
    snr(i) = mean2(images(:,:,i));
end

plot(t1,snr)
t2 = h5read('darklong.hdf5','/temp2');
%t2 = [t2;  h5read('darklong2.hdf5','/temp2')];
% 
% hold on 
% plot(t1,'.')
% plot(t2-1,'.')
% xlabel('Measurement Number')
% ylabel('FPA Temperature [deg. C]')
% title('Boson reported FPA temperature over time')
% hold off
% 
% legend('cam1','cam2')