Liste des integrations :

<details><summary> alerte_state_sensor <i>(sensors: 1)</i> </summary>
<p>

*Sensors*
- MyFox-Etat LABEL-1|state (AlerteStateSensorEntity)

</p></details>

<details><summary> camera <i>(buttons: 6, cameras: 1)</i> </summary>
<p>

*Buttons*
- MyFox-LABEL Snapshot-1|snapshot (CameraButtonEntity)
- MyFox-LABEL Rec Start-1|recording_start (CameraButtonEntity)
- MyFox-LABEL Rec Stop-1|recording_stop (CameraButtonEntity)
- MyFox-LABEL Live Start-1|live_start (CameraButtonEntity)
- MyFox-LABEL Live Extend-1|live_extend (CameraButtonEntity)
- MyFox-LABEL Live Stop-1|live_stop (CameraButtonEntity)

*Cameras*
- MyFox-LABEL-1|camera (MyFoxCameraEntity)

</p></details>

<details><summary> gate <i>(buttons: 2)</i> </summary>
<p>

*Buttons*
- MyFox-One - LABEL-1|performeOne (PerformButtonEntity)
- MyFox-Two - LABEL-1|performeTwo (PerformButtonEntity)

</p></details>

<details><summary> group_electric <i>(buttons: 2)</i> </summary>
<p>

*Buttons*
- MyFox-On LABEL-1|on (SocketButtonEntity)
- MyFox-Off LABEL-1|off (SocketButtonEntity)

</p></details>

<details><summary> group_shutter <i>(buttons: 2)</i> </summary>
<p>

*Buttons*
- MyFox-Ouverture LABEL-1|open (ShutterButtonEntity)
- MyFox-Fermeture LABEL-1|close (ShutterButtonEntity)

</p></details>

<details><summary> heater <i>(selects: 1)</i> </summary>
<p>

*Selects*
- MyFox-Consigne LABEL-1|stateLabel (HeaterSelectEntity)

</p></details>

<details><summary> librairie <i>()</i> </summary>
<p>

</p></details>

<details><summary> light <i>(sensors: 1)</i> </summary>
<p>

*Sensors*
- MyFox-Luminosité LABEL-1|light (LightSensorEntity)

</p></details>

<details><summary> module <i>(buttons: 2)</i> </summary>
<p>

*Buttons*
- MyFox-One - LABEL-1|performeOne (PerformButtonEntity)
- MyFox-Two - LABEL-1|performeTwo (PerformButtonEntity)

</p></details>

<details><summary> security <i>(alarms: 1)</i> </summary>
<p>

*Alarms*
- MyFox-Security-1|status (MyFoxAlarmEntity)

</p></details>

<details><summary> shutter <i>(buttons: 2)</i> </summary>
<p>

*Buttons*
- MyFox-Ouverture LABEL-1|open (ShutterButtonEntity)
- MyFox-Fermeture LABEL-1|close (ShutterButtonEntity)

</p></details>

<details><summary> socket <i>(buttons: 2)</i> </summary>
<p>

*Buttons*
- MyFox-On LABEL-1|on (SocketButtonEntity)
- MyFox-Off LABEL-1|off (SocketButtonEntity)

</p></details>

<details><summary> state <i>(sensors: 1)</i> </summary>
<p>

*Sensors*
- MyFox-Etat LABEL-1|stateLabel (StateSensorEntity)

</p></details>

<details><summary> temperature <i>(sensors: 1)</i> </summary>
<p>

*Sensors*
- MyFox-Temperature LABEL-1|lastTemperature (TempSensorEntity)

</p></details>

<details><summary> thermo <i>(sensors: 1, selects: 1)</i> </summary>
<p>

*Sensors*
- MyFox-Temperature LABEL-1|lastTemperature (TempSensorEntity)

*Selects*
- MyFox-Consigne-Thermo LABEL-1|stateLabel (HeaterSelectEntity)

</p></details>

<details><summary> scenario (API) <i>(scenes: 1, switches: 3)</i> </summary><p>

### scheduled

*Switches*
- MyFox-Scenario LABEL-1|enabled (ActivabledSceneEntity)

### onEvent

*Switches*
- MyFox-Scenario LABEL-2|enabled (ActivabledSceneEntity)

### simulation

*Switches*
- MyFox-Scenario LABEL-3|enabled (ActivabledSceneEntity)

### onDemand

*Scenes*
- MyFox-Scenario LABEL-4|onDemand (OnDemandSceneEntity)

</p></details>


