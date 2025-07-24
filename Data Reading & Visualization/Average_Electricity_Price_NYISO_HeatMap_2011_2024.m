clear all
close all
clc
% Initialize matrix to store monthly averages
monthly_avg = zeros(12, 14);     % 12 months x 14 years (2011–2024)

% Loop through each year
for year = 2011:2024
     % Construct file name
     filename = sprintf('USA_NYISO_%d.csv', year);
    
     % Read the file
     data = readtable(filename);
    
     % Extract timestamp and second column
     timestamps = datetime(data{:,1}, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');
     values = data{:,2};
    
     % Compute monthly averages
     for m = 1:12
     idx = month(timestamps) == m;
     monthly_avg(m, year - 2010) = mean(values(idx), 'omitnan');
     end
end

% Create heatmap
figure()
imagesc(2011:2024, 1:12, monthly_avg);
colormap('hot');
colorbar;
set(gca,'FontName','Times New Roman','FontSize',16,'TickLabelInterpreter','latex')
xlabel('Year', 'Interpreter', 'latex');
ylabel('Month', 'Interpreter', 'latex');
title('Average Price [\$/MWh] in NYISO', 'Interpreter', 'latex');
yticks(1:12);
yticklabels(cellstr(datestr(datetime(1,1:12,1), 'mmm')));

% Add value labels
for y = 1:14
     for m = 1:12
     val = monthly_avg(m, y);
     text(2010 + y, m, sprintf('%.1f', val), ...
     'HorizontalAlignment', 'center', 'Color', 'white', 'FontSize', 14, 'Interpreter', 'latex');
     end
end
