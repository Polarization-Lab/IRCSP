%% Import data
fn ="bb1.h5";
[rcam1,rcam2,t1,t2] = load_NUCdata(fn);
fn2 = "bb5.h5";
[rcam11,rcam21,t11,t21] = load_NUCdata(fn2);

%% Plot Temperatures 
figure(1)

subplot(2,1,1)
hold on
plot(t1,squeeze(rcam1(130,140,:)),'o')
plot(t11,squeeze(rcam11(130,140,:)),'o')
ylabel('pixel response [ADC]')
xlabel('FPA temperature')
%ylim([1.180e4 1.2e4])
title('Camera 1')
hold off


subplot(2,1,2)
hold on
title('Camera 2')
plot(t2,squeeze(rcam2(148,160,:)),'o')
plot(t21,squeeze(rcam21(148,160,:)),'o')
ylabel('pixel response [ADC]')
xlabel('FPA temperature')
%ylim([1.169e4 1.2e4])
hold off

%% Select which data points to use for each camera



%% Select ROI and input to NUC function

r112 = rcam1(:,:,1)-rcam1(:,:,5);
r134 = rcam1(:,:,6)-rcam1(:,:,10);
t112 = t1(1) - t1(5);
t134 = t1(6) - t1(10);


%cam 2
r212 = rcam2(:,:,1)-rcam2(:,:,5);
r212 = rcam2(:,:,6)-rcam2(:,:,10);
t212 = t2(1) - t2(5);
t234 = t2(6) - t2(10);

%% Save Computed
targets = [2,3,4,5,6,7,8,9,10];
r1=[];r2 = [];t1s=[];t2s=[];
i = 1;
% samp = 10;
% figure(2)
% subplot(2,1,1)
% hold on
% while i < samp
%     t = num2str(targets(i));
%     fn = strcat("dark",t,".h5");
%     [rcam1,rcam2,t1,t2] = load_NUCdata(fn);
%     
%     r1 = squeeze(rcam1(130,150,:));
%     ylim([1.15e4, 1.2e4])
%     plot(t1,r1,'o')
%     ylabel('focal plane temperature (^\circ  C)')
%     xlabel('measurement number')
%     i = i+1;
% end
% hold off 
% 
% 
% i = 1;
% subplot(2,1,2)
% hold on
%  while i < samp
%     t = num2str(targets(i));
%     fn = strcat("dark",t,".h5");
%     [rcam1,rcam2,t1,t2] = load_NUCdata(fn);
%     r2 = squeeze(rcam2(148,150,:));
%     plot(t2,r2,'o')
%     ylim([1.15e4 1.2e4])
%     ylabel('focal plane temperature (^\circ  C)')
%     xlabel('measurement number')
%     i = i+1;
%  end
% 
% hold off
%  
