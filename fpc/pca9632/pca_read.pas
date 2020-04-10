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
  0:   Form1.Edit11.Text := val;
  1:   Form1.Edit12.Text := val;
  2:   Form1.Edit13.Text := val;
  3:   Form1.Edit14.Text := val;
  end;

end;

procedure read_pca ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.pca9632_pkg import pca9632|' +
                      'reg_view = pca9632.read_pca9632()|' +
                      'print (":READ_PCA:{}".format(reg_view))|';

Form1.PythonEngine1.ExecStrings(Py_S);
Py_S.Free;
end;

procedure read_output_pca (pca: pca6532Ob; grpdim: DIMM; grpfreq: FREQ);
var
  i: Integer;
  x: Integer;
begin

  Form1.ComboBoxEx1.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr1.attr_val);       //ALLCALL 0-ON, 1-OFF
  Form1.ComboBoxEx2.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr2.attr_val);       //SUB3 0-ON, 1-OFF
  Form1.ComboBoxEx3.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr3.attr_val);       //SUB2 0-ON, 1-OFF
  Form1.ComboBoxEx4.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr4.attr_val);       //SUB1 0-ON, 1-OFF
  Form1.ComboBoxEx5.ItemIndex:=EnumToInt(TYPE0,pca.attr1.attr_val_obj.attr5.attr_val);       //SLEEP 0-ON, 1-OFF

  Form1.ComboBoxEx6.ItemIndex:=EnumToInt(TYPE0,pca.attr2.attr_val_obj.attr1.attr_val);       //OUTDRV 0-ON, 1-OFF
  Form1.ComboBoxEx7.ItemIndex:=EnumToInt(TYPE0,pca.attr2.attr_val_obj.attr2.attr_val);       //OCH 0-ON, 1-OFF
  Form1.ComboBoxEx8.ItemIndex:=EnumToInt(TYPE0,pca.attr2.attr_val_obj.attr3.attr_val);       //INVRT 0-ON, 1-OFF
  Form1.ComboBoxEx9.ItemIndex:=EnumToInt(TYPE1,pca.attr2.attr_val_obj.attr4.attr_val);       //DMBLNK 0-DIMMING, 1-BLINKING

  Form1.Edit1.Text:= pca.attr3.attr_val;  //PWM0
  Form1.Edit1.Alignment:=taRightJustify;
  Form1.Edit2.Text:= pca.attr4.attr_val;  //PWM1
  Form1.Edit2.Alignment:=taRightJustify;
  Form1.Edit3.Text:= pca.attr5.attr_val;  //PWM2
  Form1.Edit3.Alignment:=taRightJustify;
  Form1.Edit4.Text:= pca.attr6.attr_val;  //PWM3
  Form1.Edit4.Alignment:=taRightJustify;

  if  (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING' ) then
    for i:=1 to 16 do begin
       x := trunc(StrToFloat(pca.attr7.attr_val)) and 240;
       if grpdim[i].value = x  then
       begin
         Form1.Edit5.Text:= FloatToStr(grpdim[i].perc);  //GRPPWM in DIMMING
         Form1.Edit5.Alignment:=taRightJustify;
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
         Form1.Edit5.Text:= FloatToStr(grppwm[i].perc);  //GRPPWM in BLINKING   from 24 - 6 Hz
         Form1.Edit5.Alignment:=taRightJustify;
         break;
       end;
     end;
    end
    else begin
     Form1.Edit5.Text:= FloatToStr(RoundTo(((trunc(StrToFloat(pca.attr7.attr_val)) * 100)/256),-1));  //GRPPWM in BLINKING from 6 Hz ->
     Form1.Edit5.Alignment:=taRightJustify;
    end;
  end;

  Form1.Edit6.Text:= FloatToStr(grpfreq[StrToInt(pca.attr8.attr_val)].freq);  //GRPFREQ
  Form1.Edit15.Text:= grpfreq[StrToInt(pca.attr8.attr_val)].time;
  Form1.Edit6.Alignment:=taRightJustify;
  Form1.Edit15.Alignment:=taRightJustify;

  Form1.Edit7.Text:= pca.attr9.attr_val;  //SUBADR1
  Form1.Edit7.Alignment:=taRightJustify;
  Form1.Edit8.Text:= pca.attr10.attr_val;  //SUBADR2
  Form1.Edit8.Alignment:=taRightJustify;
  Form1.Edit9.Text:= pca.attr11.attr_val;  //SUBADR3
  Form1.Edit9.Alignment:=taRightJustify;

  Form1.ComboBoxEx10.ItemIndex:=EnumToIntLdr(pca.attr12.attr_val_obj.attr1.attr_val);       //LDR0 0-ON, 1-OFF, 2-PWM, 3-GRPPWM
  Form1.ComboBoxEx11.ItemIndex:=EnumToIntLdr(pca.attr12.attr_val_obj.attr2.attr_val);       //LDR1 0-ON, 1-OFF, 2-PWM, 3-GRPPWM
  Form1.ComboBoxEx12.ItemIndex:=EnumToIntLdr(pca.attr12.attr_val_obj.attr3.attr_val);       //LDR2 0-ON, 1-OFF, 2-PWM, 3-GRPPWM
  Form1.ComboBoxEx13.ItemIndex:=EnumToIntLdr(pca.attr12.attr_val_obj.attr4.attr_val);       //LDR3 0-ON, 1-OFF, 2-PWM, 3-GRPPWM

  if (Form1.ComboBoxEx10.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING') then  set_freq (LDR0, 3)       // dimming
  else if (Form1.ComboBoxEx10.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING') then set_freq (LDR0, 2)  // blinking
        else  set_freq (LDR0, Form1.ComboBoxEx10.ItemIndex);
  if (Form1.ComboBoxEx11.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING') then  set_freq (LDR1, 3)       // dimming
  else if (Form1.ComboBoxEx11.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING') then set_freq (LDR1, 2)  // blinking
        else  set_freq (LDR1, Form1.ComboBoxEx11.ItemIndex);
  if (Form1.ComboBoxEx12.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING') then  set_freq (LDR2, 3)       // dimming
  else if (Form1.ComboBoxEx12.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING') then set_freq (LDR2, 2)  // blinking
        else  set_freq (LDR2, Form1.ComboBoxEx12.ItemIndex);
  if (Form1.ComboBoxEx13.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING') then  set_freq (LDR3, 3)       // dimming
  else if (Form1.ComboBoxEx13.ItemIndex = 3) and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING') then set_freq (LDR3, 2)  // blinking
        else  set_freq (LDR3, Form1.ComboBoxEx13.ItemIndex);

  Form1.Edit10.Text:= pca.attr13.attr_val;  //ALLCALLADR
  Form1.Edit10.Alignment:=taRightJustify;

  sleep(1000);

end;

end.
