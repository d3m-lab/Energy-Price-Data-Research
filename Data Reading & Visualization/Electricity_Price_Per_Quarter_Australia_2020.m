clear all
close all
clc

% Load the data
data = readtable('AUSTRALIA_AEMO_2020.csv');
data.Timestamp = datetime(data.Timestamp, 'InputFormat', 'yyyy/MM/dd HH:mm:ss');

% Extract quarter
data.Quarter = quarter(data.Timestamp);

% Define zones
zones = {'NSW1', 'QLD1', 'SA1', 'TAS1', 'VIC1'};

% Compute quarterly averages
quarterly_avg = varfun(@mean, data, 'InputVariables', zones, ...
     'GroupingVariables', 'Quarter');

% Convert quarter to numeric
x = double(quarterly_avg.Quarter);

% Bar plot
figure;
bar(x, table2array(quarterly_avg(:, 3:end)));
title('Average Price per Quarter in Australia (2020)', 'Interpreter','latex');
set(gca,'FontName','Times New Roman','FontSize',12,'TickLabelInterpreter','latex')
xlabel('Quarter','Interpreter','latex');
ylabel('Average Price [AU\$/MWh]','Interpreter','latex');
xlim([0.35 4.65]);
legend(zones, 'Location', 'best');
grid on;
