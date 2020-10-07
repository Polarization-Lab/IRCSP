%% Import data
fn = "test3.h5";
[rcam1,rcam2,t1,t2] = load_NUCdata(fn);

%% Plot Temperatures 
subplot(2,1,1)
hold on
plot(t1,'.-')
plot(t2,'.-')
ylabel('focal plane temperature (^\circ  C)')
xlabel('measurement number')
hold off
legend('Camera 1','Camera 2')

subplot(2,1,2)
hold on
plot(squeeze(cam1(120,100,:)),'.-')
plot(squeeze(cam2(120,100,:)),'.-')
ylabel('avg. FPA value')
xlabel('measurement number')
hold off
legend('Camera 1','Camera 2')

%% Select which data points to use for each camera



%% Select ROI and input to NUC function
%cam 1
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