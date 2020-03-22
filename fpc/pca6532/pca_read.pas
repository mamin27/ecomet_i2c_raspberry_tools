unit pca_read;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, StrUtils,
  pca_pyth_util;

procedure read_pca ();
procedure read_output_pca (pca: pca6532Ob);

Implementation

uses pca_display;

procedure read_pca ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.pca9632_pkg import pca9632_driver|' +
                      'reg_view = pca9632_driver.read_pca9632()|' +
                      'print (":READ_PCA:{}".format(reg_view))|';

Form1.PythonEngine1.ExecStrings(Py_S);
Py_S.Free;
end;

procedure read_output_pca (pca: pca6532Ob);
begin

  //pca := StrToObj(data);

  {
  write('ATTR3: ',pca.attr3.attr_name);
  write(':',pca.attr3.attr_val);
  writeln();}

  Form1.ComboBoxEx1.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr1.attr_val);       //ALLCALL 0-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx2.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr2.attr_val);       //SUB3 2-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx3.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr3.attr_val);       //SUB2 2-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx4.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr4.attr_val);       //SUB1 2-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx5.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr5.attr_val);       //SLEEP 2-N/A, 0-ON, 1-OFF

  Form1.ComboBoxEx6.ItemIndex:=EnumToInt(pca.attr2.attr_val_obj.attr1.attr_val);       //OUTDRV 2-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx7.ItemIndex:=EnumToInt(pca.attr2.attr_val_obj.attr2.attr_val);       //OCH 2-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx8.ItemIndex:=EnumToInt(pca.attr2.attr_val_obj.attr3.attr_val);       //INVRT 2-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx9.ItemIndex:=EnumToInt(pca.attr2.attr_val_obj.attr4.attr_val);       //DMBLNK 2-N/A, 0-ON, 1-OFF

  Form1.Edit1.Text:= pca.attr3.attr_val;  //PWM0
  Form1.Edit1.Alignment:=taRightJustify;
  Form1.Edit2.Text:= pca.attr4.attr_val;  //PWM1
  Form1.Edit2.Alignment:=taRightJustify;
  Form1.Edit3.Text:= pca.attr5.attr_val;  //PWM2
  Form1.Edit3.Alignment:=taRightJustify;
  Form1.Edit4.Text:= pca.attr6.attr_val;  //PWM3
  Form1.Edit4.Alignment:=taRightJustify;
  Form1.Edit5.Text:= pca.attr7.attr_val;  //GRPPWM
  Form1.Edit5.Alignment:=taRightJustify;
  Form1.Edit6.Text:= pca.attr8.attr_val;  //GRPFREQ
  Form1.Edit6.Alignment:=taRightJustify;

  Form1.Edit7.Text:= pca.attr9.attr_val;  //SUBADR1
  Form1.Edit7.Alignment:=taRightJustify;
  Form1.Edit8.Text:= pca.attr10.attr_val;  //SUBADR2
  Form1.Edit8.Alignment:=taRightJustify;
  Form1.Edit9.Text:= pca.attr11.attr_val;  //SUBADR3
  Form1.Edit9.Alignment:=taRightJustify;

  Form1.ComboBoxEx10.ItemIndex:=EnumToInt(pca.attr12.attr_val_obj.attr1.attr_val);       //LDR0 2-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx11.ItemIndex:=EnumToInt(pca.attr12.attr_val_obj.attr2.attr_val);       //LDR1 2-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx12.ItemIndex:=EnumToInt(pca.attr12.attr_val_obj.attr3.attr_val);       //LDR2 2-N/A, 0-ON, 1-OFF
  Form1.ComboBoxEx13.ItemIndex:=EnumToInt(pca.attr12.attr_val_obj.attr4.attr_val);       //LDR3 2-N/A, 0-ON, 1-OFF

  Form1.Edit10.Text:= pca.attr13.attr_val;  //ALLCALLADR
  Form1.Edit10.Alignment:=taRightJustify;

//  Image1.Stretch:= true;
//  Image1.Proportional:= true;
//  ImageList2.GetBitmap(1,Image1.Picture.Bitmap);  }
//  ImageList2.GetBitmap(0,Image1.Picture.Bitmap);

end;

end.
