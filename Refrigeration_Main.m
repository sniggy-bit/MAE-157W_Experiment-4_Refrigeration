%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%            MAE 157W            %
%     Refrigeration Analysis     %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc; clear; close all; 
%% Data Loading and Formatting
AXV = load("Refrigeration Data  - AXV CSV.csv");
CTV = load("Refrigeration Data  - CTV CSV.csv");
TXV = load("Refrigeration Data  - TXV CSV.csv");

%%%%%%%%%%%%%%%%%% AXV FORMATTING %%%%%%%%%%%%%%%%%%%%%%%

AXV_suctionP= [2;7;15;30]; % Suction pressure [psig]
AXV_temp = AXV(:, 2:10); % temp [degC] 
AXV_gauge = AXV(:, 11:14); % gauge pressures [psi]
AXV_i = AXV(:, 15:17); % Current [A]
AXV_v = AXV(:,18); % Voltage [V]
AXV_FR = AXV(:,19); % Flow rate [lb/min]

    % NOTE: Incuded all the rows for each dataset type (e.g. temp, press,
    % current, etc.)

%%%%%%%%%%%%%%%%%% TXV FORMATTING %%%%%%%%%%%%%%%%%%%%%%%
    
    % NOTE: condition 11 = evaporator & condenser switch HIGH 
    %       condition 10 = evaporator HIGH, condenser LOW

TXV_temp11 = TXV(1, 2:10); % temp [degC] 
TXV_temp10 = TXV(2, 2:10); % temp [degC
TXV_gauge11 = TXV(1, 11:14); % gauge pressures [psi] 
TXV_gauge10 = TXV(2, 11:14); % gauge pressures [psi] 
TXV_i11 = TXV(1, 15:17); % Current [A]
TXV_i10 = TXV(2, 15:17); % Current [A]
TXV_v11 = TXV(1,18); % Voltage [V]
TXV_v10 = TXV(2,18); % Voltage [V]
TXV_FR11 = TXV(1,19); % Flow rate [lb/min]
TXV_FR10 = TXV(2,19); % Flow rate [lb/min]

%%%%%%%%%%%%%%%%%% CTV FORMATTING %%%%%%%%%%%%%%%%%%%%%%%
    % NOTE: condition 11 = evaporator & condenser switch HIGH 
    %       condition 10 = evaporator HIGH, condenser LOW
    %       condition 01 = evaporator LOW condenser HIGH 

CTV_temp11 = CTV(1, 2:10); % temp [degC] 
CTV_temp10 = CTV(2, 2:10); % temp [degC]
CTV_temp01 = CTV(3, 2:10); % temp [degC]

CTV_gauge11 = CTV(1, 11:14); % gauge pressures [psi] 
CTV_gauge10 = CTV(2, 11:14); % gauge pressures [psi] 
CTV_gauge01 = CTV(3, 11:14); % gauge pressures [psi] 


CTV_i11 = CTV(1, 15:17); % Current [A]
CTV_i10 = CTV(2, 15:17); % Current [A]
CTV_i01 = CTV(3, 15:17); % Current [A]


CTV_v11 = CTV(1,18); % Voltage [V]
CTV_v10 = CTV(2,18); % Voltage [V]
CTV_v01 = CTV(3,18); % Voltage [V]


CTV_FR11 = CTV(1,19); % Flow rate [lb/min]
CTV_FR10 = CTV(2,19); % Flow rate [lb/min]
CTV_FR01 = CTV(3,19); % Flow rate [lb/min]