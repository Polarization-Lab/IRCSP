function [] = IRCSPMMmodel(waves,D,A)
%waves: array of wavelengths, units in microns
%D: DOLP of the incoming light
%A: AOLP of the incoming light 

So1_transmission = zeros(1,length(waves));
So1_reflection = zeros(1,length(waves));%empty array of scalar valued first elements of output stokes vector
t_hor = 5010; %thickness of high order retarder, units in microns 
%CdSe crystal of thickness 5.01mm currently in IRCSP

%equations for birefringence taken from 
%"Infrared Birefringence Spectra for Cadmium Sulfide and Cadmium Selenide" 
%by David Chenault and Russel Chipman

%Coefficients for the Sellmeier Equation for CdSe
A_ne = 4.0832;
B_ne = 2.0041;
C_ne = .20646;
D_ne = 3.9928;
E_ne = 3866.92;
A_no = 4.1318;
B_no = 1.8584;
C_no = .21999;
D_no = 2.76773;
E_no = 2962.98;

for i =  1:length(waves)

%Sellmeier equation, valid for IR spectra
ne(i)= sqrt(A_ne + (B_ne*waves(i)^2)/(waves(i)^2 - C_ne) + (D_ne*waves(i)^2)/(waves(i)^2 - E_ne));
no(i) = sqrt(A_no + (B_no*waves(i)^2)/(waves(i)^2 - C_no) + (D_no*waves(i)^2)/(waves(i)^2 - E_no)); 
b(i) = ne(i) - no(i); %magntitude of birefringence
   
retardance(i) = (2*pi*b(i)*t_hor)/waves(i); %retardance spectrum

%found MM of the LP and QWP from Kira's first paper
LP_pos = [1 0 1 0; 0 0 0 0; 1 0 1 0; 0 0 0 0];  
LP_neg = [1 0 -1 0; 0 0 0 0; -1 0 1 0; 0 0 0 0];
HOR(:,:,i) = [1 0 0 0; 0 1 0 0; 0 0 cos(retardance(i)) sin(retardance(i)); 0 0 -sin(retardance(i)) cos(retardance(i))];
QWP = [1 0 0 0; 0 0 0 -1; 0 0 1 0; 0 1 0 0];
Si = [1;D*cos(2*A);D*sin(2*A);0]; %input stokes vector with given DOLP and AOLP

MM_transmission(:,:,i) = 1/2*LP_pos*HOR(:,:,i)*QWP;
MM_reflection(:,:,i) = 1/2*LP_neg*HOR(:,:,i)*QWP;%mueller matrix 
So_transmission(:,:,i) = MM_transmission(:,:,i)*Si;
So_reflection(:,:,i) = MM_reflection(:,:,i)*Si;%output stokes vector
So1_transmission(i) = So_transmission(1,1,i); %first element of the output stokes vector
So1_reflection(i) = So_reflection(1,1,i);

end

plot(waves,So1_transmission,'b-o','LineWidth',2)
hold on
plot(waves,So1_reflection,'r-o','LineWidth',2)


end
