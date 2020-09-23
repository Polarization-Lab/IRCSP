function [fn] = filename_up(cam,wavelength,temp,exposure)
%filename produces the filename in the old GSFC convention

if wavelength < 10000
    wave = strcat('0',num2str(wavelength));
else 
    wave = num2str(wavelength);  
end

c = strcat('CAM',num2str(cam));

t = strcat(num2str(temp),"C");


ang = 'angleNA';


n = num2str(exposure);

fn = strcat('polar__',c,'_',wave,'nm_',t,'_',ang,'_',n,'.tiff');


end
