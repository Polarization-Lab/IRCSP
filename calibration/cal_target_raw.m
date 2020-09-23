
center = im1center-im1cold;
left = im1left-im1cold;
right = im1right-im1cold;
 
hold on
plot(center(100:200,131),'.');
plot(left(100:200,131),'.');
plot(right(100:200,131),'.');
hold off
