clear all
close all
clc


% Read the CSV file
data = readtable('Canada_IESO_2024.csv'); % Replace with your actual file name

% Extract timestamp and price
timestamp = data{:,1};   % Assuming the first column is timestamp
price = data{:,2};   % Assuming the second column is price

% Convert timestamp to datetime if it's in string format
if iscell(timestamp) || ischar(timestamp)
     timestamp = datetime(timestamp, 'InputFormat', 'yyyy-MM-dd HH:mm:ss'); % Adjust format as needed
end

% Plot the price
figure;
plot(timestamp, price, 'b-', 'LineWidth', 1.5);
set(gca,'FontName','Times New Roman','FontSize',12,'TickLabelInterpreter','latex')
xlabel('Timestamp','Interpreter','latex');
ylabel('Price [C\$/MWh]','Interpreter','latex');
ylim([-500 1500])
title('Hourly Price in IESO, Ontario, Canada (2024)', 'Interpreter','latex');
grid on;
