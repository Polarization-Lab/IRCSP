function [fn] = filename(cam,wavelength,temp,angle,exposure)
%filename produces the filename in the old GSFC convention

if wavelength < 10000
    wave = strcat('0',num2str(wavelength));
else 
    wave = num2str(wavelength);  
end

c = strcat('CAM',num2str(cam));

t = strcat(num2str(temp),"C");


if angle <10 
    ang = strcat('angle00',num2str(angle));
elseif angle < 100
    ang = strcat('angle0',num2str(angle));
else 
    ang = strcat('angle',num2str(angle));  
end

n = num2str(exposure);

fn = strcat('polar__',c,'_',wave,'nm_',t,'_',ang,'deg',n,'.tiff');


end

