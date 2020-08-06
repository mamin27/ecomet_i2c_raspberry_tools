unit hdc1080_read;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, StrUtils,
  hdc1080_pyth_util, hdc1080_display, math;

procedure read_output_hdc (hdc: hdc1080Ob);
procedure read_hdc ();
procedure read_measure ();
procedure self_test ();
procedure read_measure_hdc  (hdc: hdc1080Ob);
function EnumToInt (Tp: Integer; S: String) : Integer;
function EnumToInt_MODE (S: String) : Integer;
function EnumToInt_HEAT (S: String) : Integer;
function IntToEnum (Tp: Integer; S: Integer) : String;
function IntToEnum_MODE (S: Integer) : String;
function IntToEnum_HEAT (S: Integer) : String;

Implementation

const

  TYPE0 = 0;
  TYPE1 = 1;

function EnumToInt (Tp: Integer; S: String) : Integer;
begin
  if Tp = 0 then begin  // TEMP
    if S = '11BIT'
      then Result := 0;
    if S = '14BIT'
      then Result := 1;
  end;
  if Tp = 1 then begin  // HMDT
    if S = '8BIT'
      then Result := 0;
    if S = '11BIT'
      then Result := 1;
    if S = '14BIT'
      then Result := 2;
  end;
end;

function IntToEnum (Tp: Integer; S: Integer) : String;
begin
  if Tp = 1 then begin  // TEMP
    if S = 0
      then Result := 'TRES_RES2';
    if S = 1
      then Result := 'TRES_RES1';
  end;
  if Tp = 0 then begin  // HMDT
    if S = 0
      then Result := 'HRES_RES3';
    if S = 1
      then Result := 'HRES_RES2';
    if S = 2
      then Result := 'HRES_RES1';
  end;
end;

function EnumToInt_MODE (S: String) : Integer;
begin
    if S = 'BOTH'
      then Result := 0;
    if S = 'ONLY'
      then Result := 1;
end;

function IntToEnum_MODE (S: Integer) : String;
begin
    if S = 0
      then Result := 'MODE_BOTH';
    if S = 1
      then Result := 'MODE_ONLY';
end;

function EnumToInt_HEAT (S: String) : Integer;
begin
    if S = 'DISABLE'
      then Result := 0;
    if S = 'ENABLE'
      then Result := 1;
end;

function IntToEnum_HEAT (S: Integer) : String;
begin
    if S = 0
      then Result := 'HEAT_DISABLE';
    if S = 1
      then Result := 'HEAT_ENABLE';
end;

procedure read_hdc ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.hdc1080_pkg import hdc1080|' +
                      'register = hdc1080.register_list()|' +
                      'if register != "" :|' +
                      '    print (":READ_HDC:{}".format(register))|' +
                      'else :|' +
                      '    print(":READ_HDC_ERR:")|';

Form_hdc1080.PythonEngine_hdc1080.ExecStrings(Py_S);
Py_S.Free;
end;

procedure read_measure ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.hdc1080_pkg import hdc1080|' +
                      'register = hdc1080.measure_list()|' +
                      'if register != "" :|' +
                      '    print (":READ_MEASURE:{}".format(register))|' +
                      'else :|' +
                      '    print (":READ_MEASURE_ERR:")|';

Form_hdc1080.PythonEngine_hdc1080.ExecStrings(Py_S);
Py_S.Free;
end;

procedure self_test ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.hdc1080_pkg import hdc1080|' +
                      'sens = hdc1080.HDC1080()|' +
                      'ret = sens.self_test()|' +
                      'if ret == 0 :|' +
                      '    print(":TEST_PASSED:")|' +
                      'else :|' +
                      '    print(":MISSING_CHIP:")|';

Form_hdc1080.PythonEngine_hdc1080.ExecStrings(Py_S);
Py_S.Free;
end;

procedure read_output_hdc (hdc: hdc1080Ob);
var
  i: Integer;
  x: Integer;
begin

  Form_hdc1080.ComboBox_hmdt.ItemIndex := EnumToInt(TYPE1,hdc.attr1.attr_val_obj.attr1.attr_val);     //HMDT 0-8BIT, 1-11BIT, 2-14BIT
  Form_hdc1080.ComboBox_temp.ItemIndex:=EnumToInt(TYPE0,hdc.attr1.attr_val_obj.attr2.attr_val);       //TEMP 0-11BIT, 1-14BIT
  Form_hdc1080.ComboBox_mode.ItemIndex:=EnumToInt_MODE(hdc.attr1.attr_val_obj.attr4.attr_val);        //MODE 0-BOTH, 1-ONLY
  Form_hdc1080.ComboBox_heating.ItemIndex:=EnumToInt_HEAT(hdc.attr1.attr_val_obj.attr5.attr_val);     //SUB1 0-DISABLE, 1-ENABLE

  Form_hdc1080.Edit_serial.Text:= hdc.attr2.attr_val_obj.attr1.attr_val;  //SERIAL
  Form_hdc1080.Edit_serial.Alignment:=taRightJustify;
  Form_hdc1080.Edit_manuf.Text:= hdc.attr2.attr_val_obj.attr2.attr_val;  //MANUFACTURER
  Form_hdc1080.Edit_manuf.Alignment:=taRightJustify;
  Form_hdc1080.Edit_devid.Text:= hdc.attr2.attr_val_obj.attr3.attr_val;  //DEVICE ID
  Form_hdc1080.Edit_devid.Alignment:=taRightJustify;

end;

procedure  read_measure_hdc  (hdc: hdc1080Ob);
var
  i: Real;
  const s: string = #$E2#$84#$83; // degree Celsius

begin
  i := StrToFloat(hdc.attr3.attr_val_obj.attr1.attr_val);
  Form_hdc1080.Edit_temp.Text:= FloatToStr(RoundTo(i,-2)) + s;  //TEMPERATURE
  Form_hdc1080.Edit_temp.Alignment:=taRightJustify;
  i := StrToFloat(hdc.attr3.attr_val_obj.attr2.attr_val);
  Form_hdc1080.Edit_hmdt.Text:= FloatToStr(RoundTo(i,-2)) + '%';  //HUMIDITY
  Form_hdc1080.Edit_hmdt.Alignment:=taRightJustify;

end;

end.

