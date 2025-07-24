clear all
close all
clc


% Define the base folder and output folder
baseFolder = 'C:\Users\mzu50xx\OneDrive - The Pennsylvania State University\Energy Price Market Data\Day Ahead Price Data_Raw\Chile';
outputFolder = 'C:\Users\mzu50xx\OneDrive - The Pennsylvania State University\Energy Price Market Data\Day Ahead Price Data_PreProcessed\Chile';

% Create output folder if it doesn't exist
if ~exist(outputFolder, 'dir')
    mkdir(outputFolder);
end

% Define the years to process
years = 2023; %2018:2024;

% Loop through each year
for y = years
    yearFolder = fullfile(baseFolder, num2str(y));
    
    % Loop through each month (assuming 12 files per year)
    for m = 1:12
        % Construct file name: e.g., cmg1801_def.xlsm
        fileName = sprintf('cmg%02d%02d_def.xlsm', mod(y, 100), m);
        filePath = fullfile(yearFolder, fileName);
    
        % Check if file exists
        if exist(filePath, 'file')
            % Read the file
            data = readtable(filePath);
    
             % Create output file name
            outputFileName = [fileName(1:end-5), '.csv']; % Replace .xlsm with .csv
            outputPath = fullfile(outputFolder, outputFileName);
        
            % Write to CSV
            writetable(data, outputPath);
        else
            fprintf('File not found: %s\n', filePath);
        end
    end
end

disp('All files processed.');

