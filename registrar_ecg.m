function registrar_ecg
    clc; clear; close all;

    % Abrir puerto y archivo
    sp = serialport("COM5",115200);
    sp.Timeout = 1;
    flush(sp);
    fid = fopen("ecg.txt","w");

  
    T = 300;     
    t0 = tic;
    buf = zeros(1,500,"uint8");

    % Preparar figura
    hRaw  = plot(buf,"b"); hold on
    hFilt = plot(buf,"r");
    ylim([0,255]); grid on

    % Bucle principal
    while toc(t0)<T
        %gggg
        n = sp.NumBytesAvailable;
        if n>0
            datos = read(sp,n,"uint8");
            fprintf(fid,"%u\n",datos);
            buf = [buf(length(datos)+1:end), datos];
            filt = movmean(buf,5);
        end
        % actualizar gráfica
        set(hRaw, "YData", buf);
        set(hFilt,"YData", filt);
        drawnow limitrate
    end

    fclose(fid);
    clear sp
end
