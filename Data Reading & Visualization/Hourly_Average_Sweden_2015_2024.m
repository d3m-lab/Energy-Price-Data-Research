clear all
close all
clc

% Get list of all relevant CSV files
files = dir('Sweden_ENTSO-E_*.csv');

% Initialize arrays
allTimestamps = [];
allPrices = [];

% Loop through each file
for k = 1:length(files)
     data = readtable(files(k).name);

     % Convert first column to datetime
     timestamps = datetime(data{:,1}, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');     % Adjust format if needed

     % Extract 4 price columns
     prices = data{:,2:5};

     % Append
     allTimestamps = [allTimestamps; timestamps];
     allPrices = [allPrices; prices];
end

% Create timetable
TT = array2timetable(allPrices, 'RowTimes', allTimestamps);
TT.Hour = hour(TT.Time);

% Initialize matrix for hourly averages (24 hours x 4 zones)
hourlyAvg = NaN(24, 4);

% Compute hourly average for each zone
for h = 0:23
     idx = TT.Hour == h;
     hourlyAvg(h+1, :) = mean(TT{idx,1:4}, 'omitnan');
end

zones = {'SE1', 'SE2', 'SE3', 'SE4'};

% Display result
disp('Hourly Average Prices (All Years):');
disp(array2table(hourlyAvg, 'VariableNames', {'Zone1','Zone2','Zone3','Zone4'}, 'RowNames', cellstr(string(0:23)')));

% Plot
figure()
plot(hourlyAvg,'-o', 'LineWidth', 1);
title('Hourly Average Price in Sweden (2015-2024)', 'Interpreter','latex');
set(gca,'FontName','Times New Roman','FontSize',12,'TickLabelInterpreter','latex')
xlabel('Hour of Day','Interpreter','latex');
ylabel('Average Price [Euro/MWh]','Interpreter','latex');
xlim([0 25]);
legend(zones, 'Location', 'northwest','Interpreter','latex');
grid on;
