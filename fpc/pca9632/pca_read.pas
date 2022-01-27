unit pca_read;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, StrUtils,
  pca_pyth_util, pca_display, math;

procedure set_freq (ldr, status: Integer);
procedure set_freq_value (ldr: Integer; val: String);
procedure read_output_pca (pca: pca6532Ob; grpdim: DIMM; grpfreq: FREQ);
procedure read_pca ();
procedure self_test ();

Implementation

//uses pca_display;

const
  LDR0 = 0;
  LDR1 = 1;
  LDR2 = 2;
  LDR3 = 3;

  TYPE0 = 0;
  TYPE1 = 1;

procedure set_freq (ldr, status: Integer);
begin
  case status of
  0: set_freq_value (ldr, '');
  1: set_freq_value (ldr, '');
  2: set_freq_value (ldr, '1.5625 kHz');
  3: set_freq_value (ldr, '6.25 kHz');
  end;
end;

procedure set_freq_value (ldr: Integer; val: String);
begin
  case ldr of
  0:   pca9632_main.Edit11.Text := val;
  1:   pca9632_main.Edit12.Text := val;
  2:   pca9632_main.Edit13.Text := val;
  3:   pca9632_main.Edit14.Text := val;
  end;

end;

procedure read_pca ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  ecomet_i2c_sensors.pca9632 import pca9632|' +
                      'reg_view = pca9632.read_pca9632()|' +
                      'if reg_view != "" :|' +
                      '      print (":READ_PCA:{}".format(reg_view))|' +
                      'else :|' +
                      '    print(":READ_PCA_ERR:")|';

pca9632_main.PythonEngine1.ExecStrings(Py_S);
Py_S.Free;
end;

procedure self_test ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  ecomet_i2c_sensors.pca9632 import pca9632|' +
                      'sens = pca9632.PCA9632()|' +
                      'ret = sens.self_test()|' +
                      'if ret == 0 :|' +
                      '    print(":TEST_PASSED:")|' +
                      'else :|' +
                      '    print(":MISSING_CHIP:")|';

pca9632_main.PythonEngine1.ExecStrings(Py_S);
Py_S.Free;
end;

procedure read_output_pca (pca: pca6532Ob; grpdim: DIMM; grpfreq: FREQ);
var
  i: Integer;
  x: Integer;
begin

  pca9632_main.ComboBoxEx1.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr1.attr_val);       //ALLCALL 0-ON, 1-OFF
  pca9632_main.ComboBoxEx2.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr2.attr_val);       //SUB3 0-ON, 1-OFF
  pca9632_main.ComboBoxEx3.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr3.attr_val);       //SUB2 0-ON, 1-OFF
  pca9632_main.ComboBoxEx4.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr4.attr_val);       //SUB1 0-ON, 1-OFF
  pca9632_main.ComboBoxEx5.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr5.attr_val);       //SLEEP 0-ON, 1-OFF

  pca9632_main.ComboBoxEx6.ItemIndex:=EnumToInt(TYPE0,pca.attr2.attr_val_obj.attr1.attr_val);       //OUTDRV 0-ON, 1-OFF
  pca9632_main.ComboBoxEx7.ItemIndex:=EnumToInt(TYPE0,pca.attr2.attr_val_obj.attr2.attr_val);       //OCH 0-ON, 1-OFF
  pca9632_main.ComboBoxEx8.ItemIndex:=EnumToInt(TYPE0,pca.attr2.attr_val_obj.attr3.attr_val);       //INVRT 0-ON, 1-OFF
  pca9632_main.ComboBoxEx9.ItemIndex:=EnumToInt(TYPE1,pca.attr2.attr_val_obj.attr4.attr_val);       //DMBLNK 0-DIMMING, 1-BLINKING

  pca9632_main.Edit1.Text:= pca.attr3.attr_val;  //PWM0
  pca9632_main.Edit1.Alignment:=taRightJustify;
  pca9632_main.Edit2.Text:= pca.attr4.attr_val;  //PWM1
  pca9632_main.Edit2.Alignment:=taRightJustify;
  pca9632_main.Edit3.Text:= pca.attr5.attr_val;  //PWM2
  pca9632_main.Edit3.Alignment:=taRightJustify;
  pca9632_main.Edit4.Text:= pca.attr6.attr_val;  //PWM3
  pca9632_main.Edit4.Alignment:=taRightJustify;

  if  (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING' ) then
    for i:=1 to 16 do begin
       x := trunc(StrToFloat(pca.attr7.attr_val)) and 240;
       if grpdim[i].value = x  then
       begin
         pca9632_main.Edit5.Text:= FloatToStr(grpdim[i].perc);  //GRPPWM in DIMMING
         pca9632_main.Edit5.Alignment:=taRightJustify;
         break;
       end;
    end
  else begin
    if grpfreq[StrToInt(pca.attr8.attr_val)].freq >= 6 then
    begin
     for i:=1 to 64 do begin
       x := trunc(StrToFloat(pca.attr7.attr_val)) and 252;
       if grppwm[i].value = x  then
       begin
         pca9632_main.Edit5.Text:= FloatToStr(grppwm[i].perc);  //GRPPWM in BLINKING   from 24 - 6 Hz
         pca9632_main.Edit5.Alignment:=taRightJustify;
         break;
       end;
     end;
    end
    else begin
     pca9632_main.Edit5.Text:= FloatToStr(RoundTo(((trunc(StrToFloat(pca.attr7.attr_val)) * 100)/256),-1));  //GRPPWM in BLINKING from 6 Hz ->
     pca9632_main.Edit5.Alignment:=taRightJustify;
    end;
  end;

  pca9632_main.Edit6.Text:= FloatToStr(grpfreq[StrToInt(pca.attr8.attr_val)].freq);  //GRPFREQ
  pca9632_main.Edit15.Text:= grpfreq[StrToInt(pca.attr8.attr_val)].time;
  pca9632_main.Edit6.Alignment:=taRightJustify;
  pca9632_main.Edit15.Alignment:=taRightJustify;

  pca9632_main.Edit7.Text:= pca.attr9.attr_val;  //SUBADR1
  pca9632_main.Edit7.Alignment:=taRightJustify;
  pca9632_main.Edit8.Text:= pca.attr10.attr_val;  //SUBADR2
  pca9632_main.Edit8.Alignment:=taRightJustify;
  pca9632_main.Edit9.Text:= pca.attr11.attr_val;  //SUBADR3
  pca9632_main.Edit9.Alignment:=taRightJustify;

  pca9632_main.ComboBoxEx10.ItemIndex:=EnumToIntLdr(pca.attr12.attr_val_obj.attr1.attr_val);       //LDR0 0-ON, 1-OFF, 2-PWM, 3-GRPPWM
  pca9632_main.ComboBoxEx11.ItemIndex:=EnumToIntLdr(pca.attr12.attr_val_obj.attr2.attr_val);       //LDR1 0-ON, 1-OFF, 2-PWM, 3-GRPPWM
  pca9632_main.ComboBoxEx12.ItemIndex:=EnumToIntLdr(pca.attr12.attr_val_obj.attr3.attr_val);       //LDR2 0-ON, 1-OFF, 2-PWM, 3-GRPPWM
  pca9632_main.ComboBoxEx13.ItemIndex:=EnumToIntLdr(pca.attr12.attr_val_obj.attr4.attr_val);       //LDR3 0-ON, 1-OFF, 2-PWM, 3-GRPPWM

  if (pca9632_main.ComboBoxEx10.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING') then  set_freq (LDR0, 3)       // dimming
  else if (pca9632_main.ComboBoxEx10.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING') then set_freq (LDR0, 2)  // blinking
        else  set_freq (LDR0, pca9632_main.ComboBoxEx10.ItemIndex);
  if (pca9632_main.ComboBoxEx11.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING') then  set_freq (LDR1, 3)       // dimming
  else if (pca9632_main.ComboBoxEx11.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING') then set_freq (LDR1, 2)  // blinking
        else  set_freq (LDR1, pca9632_main.ComboBoxEx11.ItemIndex);
  if (pca9632_main.ComboBoxEx12.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING') then  set_freq (LDR2, 3)       // dimming
  else if (pca9632_main.ComboBoxEx12.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING') then set_freq (LDR2, 2)  // blinking
        else  set_freq (LDR2, pca9632_main.ComboBoxEx12.ItemIndex);
  if (pca9632_main.ComboBoxEx13.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING') then  set_freq (LDR3, 3)       // dimming
  else if (pca9632_main.ComboBoxEx13.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING') then set_freq (LDR3, 2)  // blinking
        else  set_freq (LDR3, pca9632_main.ComboBoxEx13.ItemIndex);

  pca9632_main.Edit10.Text:= pca.attr13.attr_val;  //ALLCALLADR
  pca9632_main.Edit10.Alignment:=taRightJustify;

  sleep(1000);

end;

end.
