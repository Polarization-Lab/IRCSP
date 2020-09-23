%% sampling of data 

angles = 0:10:180;
waves = 8000:100:1300;

%% add folders to path

for i = angles
    fp = '/Volumes/Depolarization/Projects/SWIRP/GSFC_Monochomator_Data/1000C/Polarized_Sweep_ang';
    fp = strcat(fp,num2str(i));
    addpath(fp)
end


%% generate DFC
imdark =zeros(256,320, 'uint16');
for i = angles
    im = zeros(256,320, 'uint16');
    for j = [1 3]
        im = im + imread(filename(1,13000,1000,i,j));
    end
    imdark = imdark + im/3;
end

imdark = imdark/19;

imagesc(imdark)
colorbar
caxis([11500 12500])

        
    

