clear all
close all
clc


% Get list of all relevant CSV files in the current folder
files = dir('USA_NYISO_*.csv');

% Initialize storage
timestamps = {};
nyc_prices = [];

% Loop through each file
for k = 10:14%length(files)
    filename = files(k).name;
    
    % Read the table
    data = readtable(filename);
    
    % Extract the first and 11th columns
    timestamps = [timestamps; data{:,1}];
    nyc_prices = [nyc_prices; data{:,11}];
end

% Optional: convert timestamps to datetime if needed
% timestamps = datetime(timestamps, 'InputFormat', 'your_format_here');

% Display a sample
disp(timestamps(1:5));
disp(nyc_prices(1:5));


% Number of lags
numLags = 120;

% Total number of usable rows after lagging
numRows = length(nyc_prices) - numLags;

% Initialize matrix to hold lagged features
laggedData = zeros(numRows, numLags + 1); % +1 for the current value

% Fill in the lagged matrix
for i = 1:numRows
    % Lag1 is the most recent, so reverse the order
    laggedData(i, 1:numLags) = nyc_prices(i+numLags-1:-1:i);
    laggedData(i, end) = nyc_prices(i+numLags); % Current value
end

% Create corresponding timestamps for the target values
laggedTimestamps = timestamps(numLags+1:end);

% Convert to table for easier handling
laggedTable = array2table(laggedData);
laggedTable.Properties.VariableNames = ...
    [arrayfun(@(x) sprintf('Lag%d', x), 1:numLags, 'UniformOutput', false), {'Current'}];
laggedTable.Timestamp = laggedTimestamps;

% Reorder columns to have Timestamp first
laggedTable = laggedTable(:, [end, 1:end-1]);

% Display a sample
disp(head(laggedTable));


% The current value is in the last column

% Compute Pearson correlation coefficients
corrCoeffs = corr(laggedData);

% Extract correlations between each lag and the current value
pearsonCorr = corrCoeffs(1:end-1, end);

% Plot the Pearson correlation coefficients
figure;
plot(1:numLags, pearsonCorr, '-o', 'LineWidth', 1.5);
set(gca,'FontName','Times New Roman','FontSize',12,'TickLabelInterpreter','latex')
xlabel('Time-Lagged','Interpreter','latex');
ylabel('Pearson Correlation Coefficient','Interpreter','latex');
title('Pearson Correlation of Lagged Prices with Current Price (NYISO)','Interpreter','latex');
grid on


% Assuming laggedData is your matrix with numLags lagged features + current value
% Separate predictors (lagged values) and response (current value)
X = laggedData(:, 1:end-1);  % 60 lagged features
Y = laggedData(:, end);      % Current value

% Apply ReliefF algorithm
% k is the number of nearest neighbors (commonly 10)
k = 10;
[rankedIdx, featureWeights] = relieff(X, Y, k);

% Display top 10 most important lags
disp('Top 10 most important lag features:');
disp(rankedIdx(1:10));
disp('Their corresponding weights:');
disp(featureWeights(rankedIdx(1:10)));

figure()
bar(featureWeights)
set(gca,'FontName','Times New Roman','FontSize',12,'TickLabelInterpreter','latex')
xlabel('Time-Lagged','Interpreter','latex')
ylabel('Features Importance Weight','Interpreter','latex')
title('Features Importance of Lagged Prices with Current Price (NYISO)','Interpreter','latex');
grid on
