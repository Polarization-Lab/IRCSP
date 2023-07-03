%function [] = IRCSPMMmodel(D)
%waves: array of wavelengths, units in microns

%D: DOLP of the incoming light
%A: AOLP of the incoming light

D = 1;
waves = linspace(7,13,1000);
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

angles = linspace(0,180,1000);

for n = 1:length(angles)
    for i =  1:length(waves)

    %Sellmeier equation, valid for IR spectra
        ne(i)= sqrt(A_ne + (B_ne*waves(i)^2)/(waves(i)^2 - C_ne) + (D_ne*waves(i)^2)/(waves(i)^2 - E_ne));
        no(i) = sqrt(A_no + (B_no*waves(i)^2)/(waves(i)^2 - C_no) + (D_no*waves(i)^2)/(waves(i)^2 - E_no)); 
        b(i) = ne(i) - no(i); %magntitude of birefringence

        retardance(i) = (2*pi*b(i)*t_hor)/waves(i); %retardance spectrum

        a(n) = deg2rad(angles(n));
        Si(:,:,n) = [1;D*cos(2*a(n));D*sin(2*a(n));0];%input stokes vector with given DOLP and AOLP

        MM_transmission(:,:,i) = LP(0)*LR(retardance(i),0)*LR(pi/2,pi/4); % MM of the LP in Kira's first paper is a 45 LP
        MM_reflection(:,:,i) = LP(pi/2)*LR(retardance(i),0)*LR(pi/2,pi/4);
        So_transmission(:,:,i,n) = MM_transmission(:,:,i)*Si(:,:,n);
        So_reflection(:,:,i,n) = MM_reflection(:,:,i)*Si(:,:,n);%output stokes vector
        So1_transmission(i,n) = So_transmission(1,1,i,n); %first element of the output stokes vector
        So1_reflection(i,n) = So_reflection(1,1,i,n);
       % s1(i,n) = 1/2*[1 + D*sin(retardance(i) + 2*a(n))]; %matrix multiplication done by hand
       % s2(i,n) = 1/2*[1 - D*sin(retardance(i) + 2*a(n))];
        s1(i,n) = 1/2*[1 + D*sin(2*a(n))*sin(retardance(i))]; %matrix multiplication done by hand
        s2(i,n) = 1/2*[1 - D*sin(2*a(n))*sin(retardance(i))];
       
        mod(i,n) = (So1_transmission(i,n) - So1_reflection(i,n))/(So1_transmission(i,n) + So1_reflection(i,n));
    end
end

figure;
plot(waves,So1_transmission(:,251),'b-o','LineWidth',2)
hold on 
plot(waves,So1_reflection(:,251),'r-o','LineWidth',2)
title("Normalized Intensity in Both Paths AoLP = 45","FontSize",20)

figure;
mesh(angles,waves,mod)
colorbar;
colormap(flipud(redblue(100)));
set(gca,'fontsize',20)
ylabel("Wavelengths [um]") 
xlabel("AoLP [deg]")
title("Modulation Function","FontSize",20)


%figure;
%plot(waves,s1(:,251),'b-o','LineWidth',2)
%hold on 
%plot(waves,s2(:,251),'r-o','LineWidth',2)
%title("Mueller Math by Hand","FontSize",20)

%figure;
%mesh(angles,waves,s1)
%colorbar;
%colormap(flipud(redblue(100)));
%set(gca,'fontsize',20)
%ylabel("Wavelengths [um]") 
%xlabel("AoLP [deg]")
%title("Mueller Math by Hand","FontSize",20)
