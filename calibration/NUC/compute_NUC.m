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
cam1_points = [3,4,5];
cam2_points = [1,3,4];


rcam1 = cam1(3:5,:,:);
rcam2 = cam1(13:5,:,:)

%% Select ROI and input to NUC function

%% Save Computed