# difference between systemd folders


la differenza tra i file installati in /etc/systemd/system/multi-user.target.wants/ e quelli in /etc/systemd/system/ riguarda il momento e il contesto in cui vengono avviati i servizi di sistema gestiti da systemd.

/etc/systemd/system/: Questa directory è destinata a contenere i file di unità di servizio di systemd che definiscono i servizi di sistema. I file qui presenti possono essere attivati manualmente o da altri servizi, ma non vengono avviati automaticamente durante il processo di avvio del sistema. È possibile abilitare questi servizi tramite il comando systemctl enable.
/etc/systemd/system/multi-user.target.wants/: Questa directory contiene link simbolici verso i file di unità di servizio presenti in /etc/systemd/system/. I file di unità di servizio presenti qui sono quelli che sono stati esplicitamente abilitati per l'avvio multi-utente del sistema. In sostanza, questo significa che i servizi definiti da questi file saranno avviati automaticamente durante il processo di avvio del sistema, poiché sono stati associati al target multi-utente. Questo avviene tramite l'attivazione dei servizi in /etc/systemd/system/multi-user.target.wants/.

### systemd strategy

anzichè posizionare il file di servizio in 

    /etc/systemd/system/

e creare un link simbolico verso

    /etc/systemd/system/multi-user.target.wants/

utilizzo il file sorgente nella directory dell'app senza spostarlo

    systemd/aqi_luftdaten.service

ne abilito l'esecuzione e ne creo un link simbolico verso 

    /etc/systemd/system/
    /etc/systemd/system/multi-user.target.wants/

Ciò lo faccio mediante i comandi

    sudo chmod +x aqi_luftdaten.service

    ln -s /var/www/aqi_luftdaten/systemd/aqi_luftdaten.service /etc/systemd/system/
    ln -s /var/www/aqi_luftdaten/systemd/aqi_luftdaten.service /etc/systemd/system/multi-user.target.wants/