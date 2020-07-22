unit hdc1080_write;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, StrUtils,
  hdc1080_pyth_util;

type
  TDict = record
    key: String;
    kval: String;
  end;

procedure write_reg_hdc (register: String; bits: Array of String);
procedure write_conf_reg ();
function pre_write(cond1:boolean; attr:String): String;

Implementation

uses hdc1080_display;

function pre_write(cond1:boolean; attr:String): String;
begin
  if cond1 = true then
    Result := attr
  else Result := '';
end;

procedure write_reg_hdc (register: String; bits: Array of String);
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

Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.hdc1080_pkg import hdc1080|' +
                      'sens = hdc1080.HDC1080()|' +
                      'ret = sens.write_register(' + content + ')|' +
                      'print (":WRITE_REG_CONF:WRITE_CONF")|';
               //       'print (":WRITE_REG_CONF:{}".format(register)) if ret == 0 else print (":WRITE_REG_CONF_ERR:")|';

Form_hdc1080.PythonEngine_hdc1080.ExecStrings(Py_S);
Py_S.Free;
end;

procedure write_conf_reg ();
var
  conf_idx: Integer;
  conf_cmd: array [1..6] of String;
  cmd: String;
begin

  conf_idx:=0;
  cmd := pre_write(hdc.attr1.attr_val_obj.attr2.attr_chg, hdc.attr1.attr_val_obj.attr2.attr_new_val);     // test change of TEMP bit
  if cmd <> '' then begin
     conf_idx := conf_idx + 1;
     conf_cmd[conf_idx] := cmd;
     hdc.attr1.attr_val_obj.attr2.attr_chg := false;
  end;

  cmd := pre_write(hdc.attr1.attr_val_obj.attr1.attr_chg, hdc.attr1.attr_val_obj.attr1.attr_new_val);     // test change of HMDT bit
  if cmd <> '' then begin
     conf_idx := conf_idx + 1;
     conf_cmd[conf_idx] := cmd;
     hdc.attr1.attr_val_obj.attr1.attr_chg := false;
  end;
  cmd := pre_write(hdc.attr1.attr_val_obj.attr4.attr_chg, hdc.attr1.attr_val_obj.attr4.attr_new_val);     // test change of MODE bit
  if cmd <> '' then begin
     conf_idx := conf_idx + 1;
     conf_cmd[conf_idx] := cmd;
     hdc.attr1.attr_val_obj.attr4.attr_chg := false;
  end;
  cmd := pre_write(hdc.attr1.attr_val_obj.attr5.attr_chg, hdc.attr1.attr_val_obj.attr5.attr_new_val);     // test change of HEAT bit
  if cmd <> '' then begin
     conf_idx := conf_idx + 1;
     conf_cmd[conf_idx] := cmd;
     hdc.attr1.attr_val_obj.attr5.attr_chg := false;
  end;

  if conf_idx <> 0 then begin
    write_reg_hdc('CONF',conf_cmd);
  end;

end;

end.

