clear all
close all
clc

% List of years to process
years = 2018:2025;

% Initialize arrays for each zone
allHours = [];
zonePrices = cell(1, 4); % One cell per zone

for i = 1:4
     zonePrices{i} = [];
end

for year = years
     % Construct the file name
     fileName = sprintf('Brazil_ONS-CCEE_%d.csv', year);
    
     if isfile(fileName)
     % Read the CSV file
     data = readtable(fileName);
    
     % Extract timestamp and zone prices
     timestamp = datetime(data{:,1}, 'InputFormat', 'yyyy-MM-dd HH:mm:ss'); % Adjust if needed
     prices = data{:,2:5}; % Four zones
    
     % Extract hour of the day
     hourOfDay = hour(timestamp);
     allHours = [allHours; hourOfDay]; %#ok<AGROW>
    
     % Append prices for each zone
     for i = 1:4
        zonePrices{i} = [zonePrices{i}; prices(:,i)]; %#ok<AGROW>
     end
     else
         warning('File not found: %s', fileName);
     end
end

% Compute average price for each hour for each zone
avgHourlyPrice = zeros(24, 4);
for h = 0:23
     for z = 1:4
        avgHourlyPrice(h+1, z) = mean(zonePrices{z}(allHours == h), 'omitnan');
     end
end

% Plot all four zones
figure ()
hold on;
colors = lines(4);
for z = 1:4
     stairs(1:24, avgHourlyPrice(:,z), 'LineWidth', 1.5, 'Color', colors(z,:));
end
hold off;
title('Hourly Average Price in Brazil by Zone (2018-2025)', 'Interpreter','latex');
set(gca,'FontName','Times New Roman','FontSize',12,'TickLabelInterpreter','latex')
xlabel('Hour of Day','Interpreter','latex');
ylabel('Average Price [R\$/MWh]','Interpreter','latex');
xlim([0 25]);
zones = {'NORDESTE', 'NORTE', 'SUDESTE', 'SUL'};
legend(zones, 'Location', 'northwest','Interpreter','latex');
grid on;
box on;

