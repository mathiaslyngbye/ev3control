%% analysis of the performance of the line follower (turn)

path  = pwd + "/log/drive_log_speed60_turn50_tol20_turn.csv"
load(path);
test_turn = drive_log_speed60_turn50_tol20_turn;

index_start = 1; index_end = 1;


% Number of steps for each trial
while double(test_turn(index_end,1)) < double(test_turn(index_end + 1,1))    
        index_end = index_end + 1;
end

data = zeros(40,index_end-1);
time = round(test_turn(1:1:length(data),1),2);
index_end = 1;
steps = size(data);
trials = 1;

% Getting the data from test
while index_end < length(test_turn)
    
    index = 1;
    
    while double(test_turn(index_end,1)) < double(test_turn(index_end + 1,1))   
        double(test_turn(index_end,1))
        
        if index < steps(2)
            data(trials,index) = test_turn(index_end,2);
        end
        
        if index_end > length(test_turn) - 2 
                break;
        end
        
        index_end = index_end + 1;
        index = index + 1;
    end
    index_end = index_end + 1;
    index_start = index_end;
    trials = trials + 1
end 

% Plotting the error as a function of time for each trial
figure("name","Error between the light sensor readings as a function of time");
plot(time(:),data(:,:))
title("Error between the light sensor readings as a function of time");
xlabel("Time [s]");
ylabel("Error");
xlim([0 .9])
ylim([-15 40])
set(gca,'FontSize',14)


% Plotting mean error as a function of time in form of boxplots
figure("name","Boxplot of mean error between light sensor readings as a function of time");
boxplot(data);
title("Boxplot of the error between light sensor readings as a function of time");
xlabel("Time [s]");
ylabel("Error");
xticks(0:8:length(time)-1); % Spaces = 2
set(gca,'XTicklabel',time(1):0.1:time(length(time)), 'FontSize',14)
set(gca,'XTick',0:8:length(time)-1) % To change index to sec 

%% Analysis of the performance of the line follower (straight)

path = pwd + "/log/drive_log_speed60_turn45_tol20_straight.csv";
load(path);
test_turn = drive_log_speed60_turn45_tol20_straight;

index_start = 1; index_end = 1;

% Number of steps for each trial

rep = 9; %repetitions
intersections = 5; % Crossings
intersection_index = zeros(rep,intersections);

for turn = 1:rep
    for straight = 1:intersections
        while double(test_turn(index_end,1)) < double(test_turn(index_end + 1,1))    
            index_end = index_end + 1;
        end
        intersection_index(turn,straight) = index_end; 
        index_end = index_end + 1;
    end
end

for turn = 1:rep
    for straight = 1:intersections
        while double(test_turn(index_end,1)) < double(test_turn(index_end + 1,1))    
            index_end = index_end + 1;
        end
        intersection_index(turn,straight) = index_end; 
        index_end = index_end + 1;
    end
end

data = test_turn(rep,intersection_index(:,:):1:intersection_index(:,:))

% data = zeros(40,index_end-1);
% time = round(test_turn(1:1:length(data),1),2);
% index_end = 1;
% steps = size(data);
% trials = 1;

% % Getting the data from test
% while index_end < length(test_turn) && trials < 41
%     
%     index = 1;
%     
%     while double(test_turn(index_end,1)) < double(test_turn(index_end + 1,1))   
%         double(test_turn(index_end,1))
%         
%         if index < steps(2)
%             data(trials,index) = test_turn(index_end,2);
%         end
%         
%         if index_end > length(test_turn) - 2 
%                 break;
%         end
%         
%         index_end = index_end + 1;
%         index = index + 1;
%     end
%     index_end = index_end + 1;
%     index_start = index_end;
%     trials = trials + 1
% end 
% 
% % Plotting the error as a function of time for each trial
% figure("name","Error light between sensor readings as a function of time");
% plot(time(:),data(:,:))
% title("Error as a function of time");
% xlabel("Time [s]","fontsize",18);
% ylabel("Error","fontsize",18);
% xlim([0 .9])
% ylim([-15 40])
% 
% % Plotting mean error as a function of time in form of boxplots
% figure("name","Boxplot of mean error between light sensor readings as a function of time");
% boxplot(data);
% title("Boxplot of the error between light sensor readings as a function of time");
% xlabel("Time [s]","fontsize",18);
% ylabel("Error","fontsize",18);
% xticks(0:8:length(time)-1); % Spaces = 2
% set(gca,'XTicklabel',time(1):0.1:time(length(time)))
% set(gca,'XTick',0:8:length(time)-1) % To change index to sec 