%%

path  = pwd + "/log/drive_log.csv";
load(path);

index = 0;


while 1
    
    line = [0 0];
    
    while drive_log(index,1) < drive_log(index+1,1)
        
        
    end 
    index = index + 1;
    
end 

scatter(drive_log(:,1),drive_log(:,2))