function [cam1,cam2,t1,t2] = load_NUCdata(fn)
%load_NUCdata
%   Detailed explanation goes here

cam1 = h5read(fn,'/imgs1');
cam2 = h5read(fn,'/imgs2');
t1 = h5read(fn,'/temps1');
t2 = h5read(fn,'/temps2');
end

