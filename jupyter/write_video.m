function video = write_video(fp)

%this script takes a filepath to data and stiches images together into a
%video. Lines 21 and 28 will need to be edited depending on how the data is
%organized in the filepath

fp = 'C:\Users\khart\Documents\IRCSP2_data\Jaclyn\mono_response\polarized_8_12microns\';
fn = 'ImageAnimation';
wvs = 8:.25:12;
num_wvs = length(wvs);
degs = [0 45 90 135];
num_deg = length(degs);

video = VideoWriter(strcat(fp,fn,'-.mp4'),'MPEG-4');
video.FrameRate = 16/15;
open(video);
set(0,'DefaultFigureVisible', 'off');
    
    for i = 1:num_wvs
        for j = 1:num_deg
    images = h5read(strcat(fp,num2str(wvs(i)),'microns\',num2str(degs(j)),'deg.h5'),'/imgs1');
    images = imrotate(images,270);
    images = flipdim(images ,2); 
    imagesc(images)
    colorbar;
    caxis([23000 23800])
    title(strcat('Wavelength = ',num2str(wvs(i)),'microns and  ',' LP =  ',num2str(degs(j)),'deg'))
    axis equal;
    axis off;
    frame = getframe(gcf);
    writeVideo(video,frame)
        end
    end

close(video)


end