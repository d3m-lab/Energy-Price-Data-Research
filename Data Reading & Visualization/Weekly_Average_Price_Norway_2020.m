clear all 
close all
clc

% Load the data
data = readtable('Norway_ENTSO-E_2020.csv');
data.Timestamp = datetime(data.Timestamp, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');

% Define Norwegian zones
zones = {'NO1', 'NO2', 'NO3', 'NO4', 'NO5'};

% Extract week start date
data.Week = dateshift(data.Timestamp, 'start', 'week');

% Compute weekly averages
weekly_avg = varfun(@mean, data, 'InputVariables', zones, ...
     'GroupingVariables', 'Week');

% Plot staircase (step) plot
% 
figure();
hold on;
for i = 1:length(zones)
     stairs(weekly_avg.Week, weekly_avg{:, i+2}, 'DisplayName', zones{i}, 'LineWidth', 1.5);
end
hold off;
set(gca,'FontName','Times New Roman','FontSize',12,'TickLabelInterpreter','latex')
title('Weekly Average Prices in Norway (2020)', 'Interpreter', 'latex');
xlabel('Month','Interpreter','latex');
ylabel('Average Price [Euro/MWh]','Interpreter','latex');
legend('Location', 'best');
grid on;
box on;
xlim([datetime(2020,1,1), datetime(2020,12,31)]);
xticklabels({'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});
xticks(datetime(2020,1:12,1));
