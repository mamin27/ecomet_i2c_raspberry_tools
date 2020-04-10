unit pca_write;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, StrUtils,
  pca_pyth_util;

type
  TDict = record
    key: String;
    kval: String;
  end;

procedure write_reg_pca (register: String; bits: Array of String);
procedure write_led_reg_pca (register: String; bits: Array of TDict);
procedure write_pwm_reg_pca (register: String; bits: TDict);
function pre_write(cond1:boolean; cond2,attr:String): String;
function pre_write_dmblnk(cond1:boolean; cond2,attr:String): String;
function pre_wr_led(cond1:boolean; cond2,attr:String): TDict;
procedure write_mode1_reg ();
procedure write_mode2_reg ();
procedure write_ledout_reg ();
//procedure write_output_pca (pca: pca6532Ob);

Implementation

uses pca_display;

procedure write_reg_pca (register: String; bits: Array of String);
var
  Py_S: TStringList;
  content: String[100];
  i: Integer;
begin
content := 'register = ' + #39 + register + #39 + ', bits = [';
i := 0;
repeat
   content := content + #39 + bits[i] + #39 + ',';
   i := i + 1;
until  bits[i] = '';

content := Copy(content,0,Length(content)-1);
content := content + ']';

writeln('Content: ' + content);


Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.pca9632_pkg import pca9632|' +
                      'pwm = pca9632.PCA9632()|' +
                      'ret = pwm.write_register(' + content + ')|' +
                      'print (":WRITE_REG_PCA_0:") if ret == 0 else print (":WRITE_REG_PCA_1:")|';

Form1.PythonEngine1.ExecStrings(Py_S);
Py_S.Free;
end;

procedure write_led_reg_pca (register: String; bits: Array of TDict);
var
  Py_S: TStringList;
  content: String[100];
  i: Integer;
begin
content := 'register = ' + #39 + register + #39 + ', bits = [';
i := 0;
repeat
   content := content + '{' + #39 + bits[i].key + #39 +  ' : ' + #39 + bits[i].kval + #39 + '}' + ',';
   i := i + 1;
until  bits[i].key = '';

content := Copy(content,0,Length(content)-1);
content := content + ']';
writeln(content);


Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.pca9632_pkg import pca9632|' +
                      'pwm = pca9632.PCA9632()|' +
                      'ret = pwm.write_register(' + content + ')|' +
                      'print (":WRITE_REG_PCA_0:") if ret == 0 else print (":WRITE_REG_PCA_1:")|';

Form1.PythonEngine1.ExecStrings(Py_S);
Py_S.Free;
end;

function pre_write(cond1:boolean; cond2,attr:String): String;
begin
  if cond1 = true then begin
    if cond2 = 'ON'
      then Result := attr
      else Result := attr + '_N';
  end
  else Result := '';
end;

function pre_write_dmblnk(cond1:boolean; cond2,attr:String): String;
begin
  if cond1 = true then begin
    if cond2 = 'DIMMING'
      then Result := 'DMBLNK_DIMMING'
      else Result := 'DMBLNK_BLINKING';
  end
  else Result := '';
end;

function pre_wr_led(cond1:boolean; cond2,attr:String): TDict;
var
  Dict: TDict;
begin
  Dict.key := attr;
  if cond1 = true then begin
    case cond2 of
    'ON':     Dict.kval := 'ON';
    'OFF':    Dict.kval := 'OFF';
    'PWM':    Dict.kval := 'PWM';
    'GRP':    Dict.kval := 'PWM_GRPPWM';
    end;
    Result := Dict;
  end
  else Result.key := '';
end;

procedure write_pwm_reg_pca (register: String; bits: TDict);
var
  Py_S: TStringList;
  content: String[100];
begin
content := 'register = ' + #39 + register + #39 + ', bits = [';
content := content + '{' + #39 + bits.key + #39 + ' : ' +  #39 + bits.kval +  #39 +'}' + ',';

content := Copy(content,0,Length(content)-1);
content := content + ']';
writeln(content);


Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
if bits.key = 'PWM' then
  Py_S.DelimitedText := 'from  i2c_pkg.pca9632_pkg import pca9632|' +
                        'pwm = pca9632.PCA9632()|' +
                        'ret = pwm.write_register(' + content + ')|' +
                        'print (":WRITE_REG_PWM_0:") if ret == 0 else print (":WRITE_REG_PWM_1:")|';
if bits.key = 'SGRPPWM' then
 Py_S.DelimitedText := 'from  i2c_pkg.pca9632_pkg import pca9632|' +
                        'pwm = pca9632.PCA9632()|' +
                        'ret = pwm.write_register(' + content + ')|' +
                        'print (":WRITE_REG_SGRPPWM_0:") if ret == 0 else print (":WRITE_REG_SGRPPWM_1:")|';
if bits.key = 'GRPPWM' then
 Py_S.DelimitedText := 'from  i2c_pkg.pca9632_pkg import pca9632|' +
                        'pwm = pca9632.PCA9632()|' +
                        'ret = pwm.write_register(' + content + ')|' +
                        'print (":WRITE_REG_GRPPWM_0:") if ret == 0 else print (":WRITE_REG_GRPPWM_1:")|';
if bits.key = 'GRPFREQ' then
 Py_S.DelimitedText := 'from  i2c_pkg.pca9632_pkg import pca9632|' +
                        'pwm = pca9632.PCA9632()|' +
                        'ret = pwm.write_register(' + content + ')|' +
                        'print (":WRITE_REG_GRPFREQ_0:") if ret == 0 else print (":WRITE_REG_GRPFREQ_1:")|';

Form1.PythonEngine1.ExecStrings(Py_S);
Py_S.Free;
end;

procedure write_mode1_reg ();
var
  mode1_idx: Integer;
  mode1_cmd: array [1..6] of String;
  cmd: String;
begin
   mode1_idx:=0;
  cmd := pre_write(pca.attr1.attr_val_obj.attr1.attr_chg, pca.attr1.attr_val_obj.attr1.attr_new_val, pca.attr1.attr_val_obj.attr1.attr_name);
  if cmd <> '' then begin
     mode1_idx := mode1_idx + 1;
     mode1_cmd[mode1_idx] := cmd;
     pca.attr1.attr_val_obj.attr1.attr_chg := false;
     Form1.Shape1.Visible:=false;
  end;

  cmd := pre_write(pca.attr1.attr_val_obj.attr2.attr_chg, pca.attr1.attr_val_obj.attr2.attr_new_val, pca.attr1.attr_val_obj.attr2.attr_name);
  if cmd <> '' then begin
     mode1_idx := mode1_idx + 1;
     mode1_cmd[mode1_idx] := cmd;
     pca.attr1.attr_val_obj.attr2.attr_chg := false;
     Form1.Shape2.Visible:=false;
  end;
  cmd := pre_write(pca.attr1.attr_val_obj.attr3.attr_chg, pca.attr1.attr_val_obj.attr3.attr_new_val, pca.attr1.attr_val_obj.attr3.attr_name);
  if cmd <> '' then begin
     mode1_idx := mode1_idx + 1;
     mode1_cmd[mode1_idx] := cmd;
     pca.attr1.attr_val_obj.attr3.attr_chg := false;
     Form1.Shape3.Visible:=false;
  end;
  cmd := pre_write(pca.attr1.attr_val_obj.attr4.attr_chg, pca.attr1.attr_val_obj.attr4.attr_new_val, pca.attr1.attr_val_obj.attr4.attr_name);
  if cmd <> '' then begin
     mode1_idx := mode1_idx + 1;
     mode1_cmd[mode1_idx] := cmd;
     pca.attr1.attr_val_obj.attr4.attr_chg := false;
     Form1.Shape4.Visible:=false;
  end;
  cmd := pre_write(pca.attr1.attr_val_obj.attr5.attr_chg, pca.attr1.attr_val_obj.attr5.attr_new_val, pca.attr1.attr_val_obj.attr5.attr_name);
  if cmd <> '' then begin
     mode1_idx := mode1_idx + 1;
     mode1_cmd[mode1_idx] := cmd;
     pca.attr1.attr_val_obj.attr5.attr_chg := false;
     Form1.Shape5.Visible:=false;
  end;

  if mode1_idx <> 0 then begin
    write_reg_pca('MODE1',mode1_cmd);
  end;

end;

procedure write_mode2_reg ();
var
  mode2_idx: Integer;
  mode2_cmd: array [1..5] of String;
  cmd: String;
begin
   mode2_idx:=0;
  cmd := pre_write(pca.attr2.attr_val_obj.attr1.attr_chg, pca.attr2.attr_val_obj.attr1.attr_new_val, pca.attr2.attr_val_obj.attr1.attr_name);
  if cmd <> '' then begin
     mode2_idx := mode2_idx + 1;
     mode2_cmd[mode2_idx] := cmd;
     pca.attr2.attr_val_obj.attr1.attr_chg := false;
     Form1.Shape6.Visible:=false;
  end;

  cmd := pre_write(pca.attr2.attr_val_obj.attr2.attr_chg, pca.attr2.attr_val_obj.attr2.attr_new_val, pca.attr2.attr_val_obj.attr2.attr_name);
  if cmd <> '' then begin
     mode2_idx := mode2_idx + 1;
     mode2_cmd[mode2_idx] := cmd;
     pca.attr2.attr_val_obj.attr2.attr_chg := false;
     Form1.Shape7.Visible:=false;
  end;
  cmd := pre_write(pca.attr2.attr_val_obj.attr3.attr_chg, pca.attr2.attr_val_obj.attr3.attr_new_val, pca.attr2.attr_val_obj.attr3.attr_name);
  if cmd <> '' then begin
     mode2_idx := mode2_idx + 1;
     mode2_cmd[mode2_idx] := cmd;
     pca.attr2.attr_val_obj.attr3.attr_chg := false;
     Form1.Shape8.Visible:=false;
  end;
  cmd := pre_write_dmblnk(pca.attr2.attr_val_obj.attr4.attr_chg, pca.attr2.attr_val_obj.attr4.attr_new_val, pca.attr2.attr_val_obj.attr4.attr_name);
  if cmd <> '' then begin
     mode2_idx := mode2_idx + 1;
     mode2_cmd[mode2_idx] := cmd;
     pca.attr2.attr_val_obj.attr4.attr_chg := false;
     Form1.Shape9.Visible:=false;
  end;

  if mode2_idx <> 0 then begin
    write_reg_pca('MODE2',mode2_cmd);
  end;

end;

procedure write_ledout_reg ();
var
  ledout_idx: Integer;
  ledout_cmd: array [1..5] of TDict;
  cmd: TDict;
begin

   ledout_idx:=0;
  cmd := pre_wr_led(pca.attr12.attr_val_obj.attr1.attr_chg, pca.attr12.attr_val_obj.attr1.attr_new_val, pca.attr12.attr_val_obj.attr1.attr_name);
  if cmd.key <> '' then begin
     ledout_idx := ledout_idx + 1;
     ledout_cmd[ledout_idx] := cmd;
     pca.attr12.attr_val_obj.attr1.attr_chg := false;
     Form1.Shape20.Visible:=false;
  end;
  cmd := pre_wr_led(pca.attr12.attr_val_obj.attr2.attr_chg, pca.attr12.attr_val_obj.attr2.attr_new_val, pca.attr12.attr_val_obj.attr2.attr_name);
  if cmd.key <> '' then begin
     ledout_idx := ledout_idx + 1;
     ledout_cmd[ledout_idx] := cmd;
     pca.attr12.attr_val_obj.attr2.attr_chg := false;
     Form1.Shape21.Visible:=false;
  end;
  cmd := pre_wr_led(pca.attr12.attr_val_obj.attr3.attr_chg, pca.attr12.attr_val_obj.attr3.attr_new_val, pca.attr12.attr_val_obj.attr3.attr_name);
  if cmd.key <> '' then begin
     ledout_idx := ledout_idx + 1;
     ledout_cmd[ledout_idx] := cmd;
     pca.attr12.attr_val_obj.attr3.attr_chg := false;
     Form1.Shape22.Visible:=false;
  end;
  cmd := pre_wr_led(pca.attr12.attr_val_obj.attr4.attr_chg, pca.attr12.attr_val_obj.attr4.attr_new_val, pca.attr12.attr_val_obj.attr4.attr_name);
  if cmd.key <> '' then begin
     ledout_idx := ledout_idx + 1;
     ledout_cmd[ledout_idx] := cmd;
     pca.attr12.attr_val_obj.attr4.attr_chg := false;
     Form1.Shape23.Visible:=false;
  end;

  if ledout_idx <> 0 then begin
    write_led_reg_pca('LEDOUT',ledout_cmd);
  end;

end;

end.
