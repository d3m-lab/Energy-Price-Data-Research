clear all
close all
clc


% Get list of all relevant CSV files
files = dir('SINGAPORE_NEMS_*.csv');
% Define years and initialize matrix
years = 2020:2024; % SINGAPORE_NEMS

monthlyMatrix = NaN(length(years), 12); % Rows: years, Columns: months

% Loop through each file
for k = 1:length(files)
 % Extract year from filename
 fname = files(k).name;
 yearStr = regexp(fname, '\d{4}', 'match');
 year = str2double(yearStr{1});
 rowIdx = find(years == year);
 
 % Read the CSV file
 data = readtable(fname, 'ReadVariableNames', false);
 
 % Convert timestamps and filter valid prices
 timestamps = datetime(data{:,1}, 'InputFormat', 'dd-MM-yyyy HH:mm:ss');
 prices = data{:,2};
 validIdx = ~isnan(prices);
 timestamps = timestamps(validIdx);
 prices = prices(validIdx);
 
 sum(validIdx);

 validIdxNaN = isnan(prices);
 sum(validIdxNaN);

 % Create timetable and compute monthly averages
 TT = timetable(timestamps, prices);
 monthlyTT = retime(TT, 'monthly', 'mean');
 
 % Fill matrix
 for i = 1:height(monthlyTT)
     m = month(monthlyTT.timestamps(i));
     monthlyMatrix(rowIdx, m) = monthlyTT.prices(i);
 end
end


figure()
violinplot(monthlyMatrix,'LineWidth',1.5)
title('Monthly Average Prices in Singapore (2018-2025)', 'Interpreter','latex');
set(gca,'FontName','Times New Roman','FontSize',12,'TickLabelInterpreter','latex')
xlabel('Month', 'Interpreter', 'latex');
ylabel('Average Price [S\$/MWh]', 'Interpreter', 'latex');
xticklabels({'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'});
grid on;
box on

% Export directly to vector PDF
exportgraphics(gcf, 'violin_plot.pdf', 'ContentType', 'vector');

