package com.example.jva_iot;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;


////////////////////LAB4////////////////////////////
public class MainActivity extends AppCompatActivity {
    MQTTHelper mqttHelper;
    TextView txtTemp, txtLight, txtMois;
    LabeledSwitch ledbutton1, pumpbutton2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        txtTemp = findViewById(R.id.Temperature);
        txtLight = findViewById(R.id.Light);
        txtMois = findViewById(R.id.Moisure);
        ledbutton1 = findViewById(R.id.ledbutton1);
        pumpbutton2 = findViewById(R.id.pumpbutton2);

        ledbutton1.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn == true){
                    sendDataMQTT("sonlam7220/feeds/button1","1");
                }
                else{
                    sendDataMQTT("sonlam7220/feeds/button1","0");
                }
            }
        });
        pumpbutton2.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn == true){
                    sendDataMQTT("sonlam7220/feeds/button2","1");
                }
                else{
                    sendDataMQTT("sonlam7220/feeds/button2","0");
                }
            }
        });
        startMQTT();
    }
    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        }catch (MqttException e){
        }
    }
    public void startMQTT(){
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST", topic + "***" + message.toString());
                if(topic.contains("sensor1")){
                    txtTemp.setText(message.toString() + "°F");
                }
                else if(topic.contains("sensor2")){
                    txtLight.setText(message.toString());
                }
                else if(topic.contains("sensor3")){
                    txtMois.setText(message.toString() + "%");
                }
                else if(topic.contains("button1")){
                    if(message.toString().equals("1")){
                        ledbutton1.setOn(true);
                    }
                    else{
                        ledbutton1.setOn(false);
                    }
                }
                else if(topic.contains("button2")){
                    if(message.toString().equals("1")){
                        pumpbutton2.setOn(true);
                    }
                    else{
                        pumpbutton2.setOn(false);
                    }
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}