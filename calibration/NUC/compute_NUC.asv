%% Import data
fn = "test3.h5";
[cam1,cam2,t1,t2] = load_NUCdata(fn);

%% Plot Temperatures 
hold on
plot(t1,'.-')
plot(t2,'.-')
ylabel('focal plane temperature (^\circ  C)')
xlabel('measurement number')
hold off
legend('Camera 1','Camera 2')

%% Select which data points to use for each camera
rcam1 = cam1(1:4,:,:);
rcam2 = cam1(1:4,:,:);

t1s = t1(1:4);
t2s = t2(1:4);

%% Select ROI and input to NUC function
%cam 1
r112 = rcam1(1,:,:)-rcam1(2,:,:);
r134 = rcam1(3,:,:)-rcam1(4,:,:);
t112 = t1s(1) - t1s(2);
t134 = t1s(3) - t1s(4);


%cam 2
r212 = rcam2(1,:,:)-rcam2(2,:,:);
r212 = rcam2(3,:,:)-rcam2(4,:,:);
t212 = t2s(1) - t2s(2);
t234 = t2s(3) - t2s(4);

%% Save Computed