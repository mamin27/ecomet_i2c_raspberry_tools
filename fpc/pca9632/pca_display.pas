unit pca_display;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, Buttons,
  ComboEx, ComCtrls, ExtCtrls, Spin, Types, StrUtils, PythonEngine,
  pca_pyth_util;

type

  { TForm1 }

  TForm1 = class(TForm)
    ComboBoxEx1: TComboBoxEx;
    ComboBoxEx10: TComboBoxEx;
    ComboBoxEx11: TComboBoxEx;
    ComboBoxEx12: TComboBoxEx;
    ComboBoxEx13: TComboBoxEx;
    ComboBoxEx2: TComboBoxEx;
    ComboBoxEx3: TComboBoxEx;
    ComboBoxEx4: TComboBoxEx;
    ComboBoxEx5: TComboBoxEx;
    ComboBoxEx6: TComboBoxEx;
    ComboBoxEx7: TComboBoxEx;
    ComboBoxEx8: TComboBoxEx;
    ComboBoxEx9: TComboBoxEx;
    Edit1: TEdit;
    Edit10: TEdit;
    Edit2: TEdit;
    Edit3: TEdit;
    Edit4: TEdit;
    Edit5: TEdit;
    Edit6: TEdit;
    Edit7: TEdit;
    Edit8: TEdit;
    Edit9: TEdit;
    Image1: TImage;
    ImageList1: TImageList;
    ImageList2: TImageList;
    PythonEngine1: TPythonEngine;
    PythonInputOutput1: TPythonInputOutput;
    StaticText1: TStaticText;
    StaticText10: TStaticText;
    StaticText11: TStaticText;
    StaticText12: TStaticText;
    StaticText13: TStaticText;
    StaticText14: TStaticText;
    StaticText15: TStaticText;
    StaticText16: TStaticText;
    StaticText17: TStaticText;
    StaticText18: TStaticText;
    StaticText19: TStaticText;
    StaticText2: TStaticText;
    StaticText20: TStaticText;
    StaticText21: TStaticText;
    StaticText22: TStaticText;
    StaticText23: TStaticText;
    StaticText24: TStaticText;
    StaticText25: TStaticText;
    StaticText26: TStaticText;
    StaticText27: TStaticText;
    StaticText28: TStaticText;
    StaticText3: TStaticText;
    StaticText4: TStaticText;
    StaticText5: TStaticText;
    StaticText6: TStaticText;
    StaticText7: TStaticText;
    StaticText8: TStaticText;
    StaticText9: TStaticText;
    ToggleBox1: TToggleBox;
    TrackBar1: TTrackBar;
    procedure PythonInputOutput1SendData(Sender: TObject; const Data: AnsiString);
    procedure Edit1Click(Sender: TObject);
    procedure Edit2Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure RadioButton1Change(Sender: TObject);
  private
  public
    procedure DoPy_InitEngine;

  end;

var
  Form1: TForm1;
  ItemEx010,ItemEx011,ItemEx012: TComboExItem;
  ItemEx020,ItemEx021,ItemEx022: TComboExItem;
  ItemEx030,ItemEx031,ItemEx032: TComboExItem;
  ItemEx040,ItemEx041,ItemEx042: TComboExItem;
  ItemEx050,ItemEx051,ItemEx052: TComboExItem;

  ItemEx060,ItemEx061,ItemEx062: TComboExItem;
  ItemEx070,ItemEx071,ItemEx072: TComboExItem;
  ItemEx080,ItemEx081,ItemEx082: TComboExItem;
  ItemEx090,ItemEx091,ItemEx092: TComboExItem;

  ItemEx100,ItemEx101,ItemEx102: TComboExItem;
  ItemEx110,ItemEx111,ItemEx112: TComboExItem;
  ItemEx120,ItemEx121,ItemEx122: TComboExItem;
  ItemEx130,ItemEx131,ItemEx132: TComboExItem;

  pca: pca6532Ob;
  pca_attr: PyRecordOb;
  pca_c:  pca6532Ob_c;
  pca_c_attr: PyRecordOb_c;
  Ob_pca_c_attr: array[1..50] of PyRecordOb_c;
  Ob_pca_attr: array[1..50] of PyRecordOb;
  Ob_pca_c: array[1..50] of pca6532Ob_c;

  procedure ComboBox_init (Item1, Item2: TComboExItem; ComboBoxEx: TComboBoxEx);
  function EnumToInt (S: String) : Integer;

implementation

const
  cPyLibraryLinux = 'libpython3.7m.so.1.0';

{$R *.lfm}

{ TForm1 }

procedure ComboBox_init (Item1, Item2: TComboExItem; ComboBoxEx: TComboBoxEx);
begin
  {
  Item0 := ComboBoxEx.ItemsEx.Add;
  Item0.Caption:= '';
  Item0.Index:=2; }
  Item1 := ComboBoxEx.ItemsEx.Add;
  Item1.Caption:= '';
  Item1.ImageIndex:=0;
  Item1.Index:=0;
  Item2 := ComboBoxEx.ItemsEx.Add;
  Item2.Caption:= '';
  Item2.ImageIndex:=1;
  Item2.Index:=1;
end;

function EnumToInt (S: String) : Integer;
begin
  if S = 'ON'
    then Result := 0;
  if S = 'OFF'
    then Result := 1;
end;

procedure TForm1.PythonInputOutput1SendData(Sender: TObject;
  const Data: AnsiString);
begin

  pca := StrToObj(data);

  write('ATTR3: ',pca.attr3.attr_name);
  write(':',pca.attr3.attr_val);
  writeln();

  ComboBoxEx1.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr1.attr_val);       //ALLCALL 0-N/A, 0-ON, 1-OFF
  ComboBoxEx2.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr2.attr_val);       //SUB3 2-N/A, 0-ON, 1-OFF
  ComboBoxEx3.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr3.attr_val);       //SUB2 2-N/A, 0-ON, 1-OFF
  ComboBoxEx4.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr4.attr_val);       //SUB1 2-N/A, 0-ON, 1-OFF
  ComboBoxEx5.ItemIndex:=EnumToInt(pca.attr1.attr_val_obj.attr5.attr_val);       //SLEEP 2-N/A, 0-ON, 1-OFF

  ComboBoxEx6.ItemIndex:=EnumToInt(pca.attr2.attr_val_obj.attr1.attr_val);       //OUTDRV 2-N/A, 0-ON, 1-OFF
  ComboBoxEx7.ItemIndex:=EnumToInt(pca.attr2.attr_val_obj.attr2.attr_val);       //OCH 2-N/A, 0-ON, 1-OFF
  ComboBoxEx8.ItemIndex:=EnumToInt(pca.attr2.attr_val_obj.attr3.attr_val);       //INVRT 2-N/A, 0-ON, 1-OFF
  ComboBoxEx9.ItemIndex:=EnumToInt(pca.attr2.attr_val_obj.attr4.attr_val);       //DMBLNK 2-N/A, 0-ON, 1-OFF

  Edit1.Text:= pca.attr3.attr_val;  //PWM0
  Edit1.Alignment:=taRightJustify;
  Edit2.Text:= pca.attr4.attr_val;  //PWM1
  Edit2.Alignment:=taRightJustify;
  Edit3.Text:= pca.attr5.attr_val;  //PWM2
  Edit3.Alignment:=taRightJustify;
  Edit4.Text:= pca.attr6.attr_val;  //PWM3
  Edit4.Alignment:=taRightJustify;
  Edit5.Text:= pca.attr7.attr_val;  //GRPPWM
  Edit5.Alignment:=taRightJustify;
  Edit6.Text:= pca.attr8.attr_val;  //GRPFREQ
  Edit6.Alignment:=taRightJustify;

  Edit7.Text:= pca.attr9.attr_val;  //SUBADR1
  Edit7.Alignment:=taRightJustify;
  Edit8.Text:= pca.attr10.attr_val;  //SUBADR2
  Edit8.Alignment:=taRightJustify;
  Edit9.Text:= pca.attr11.attr_val;  //SUBADR3
  Edit9.Alignment:=taRightJustify;

  ComboBoxEx10.ItemIndex:=EnumToInt(pca.attr12.attr_val_obj.attr1.attr_val);       //LDR0 2-N/A, 0-ON, 1-OFF
  ComboBoxEx11.ItemIndex:=EnumToInt(pca.attr12.attr_val_obj.attr2.attr_val);       //LDR1 2-N/A, 0-ON, 1-OFF
  ComboBoxEx12.ItemIndex:=EnumToInt(pca.attr12.attr_val_obj.attr3.attr_val);       //LDR2 2-N/A, 0-ON, 1-OFF
  ComboBoxEx13.ItemIndex:=EnumToInt(pca.attr12.attr_val_obj.attr4.attr_val);       //LDR3 2-N/A, 0-ON, 1-OFF

  Edit10.Text:= pca.attr13.attr_val;  //ALLCALLADR
  Edit10.Alignment:=taRightJustify;

  Image1.Stretch:= true;
  Image1.Proportional:= true;
  ImageList2.GetBitmap(1,Image1.Picture.Bitmap);
//  ImageList2.GetBitmap(0,Image1.Picture.Bitmap);

end;

procedure TForm1.DoPy_InitEngine;
var
  S: string;
begin
  S:=
    {$ifdef linux} cPyLibraryLinux {$endif};
  PythonEngine1.DllPath:= ExtractFileDir(S);
  PythonEngine1.DllName:= ExtractFileName(S);
  PythonEngine1.LoadDll;
end;

procedure TForm1.FormCreate(Sender: TObject);
var
  i : Integer;
  Py_S: TStringList;
begin

  DoPy_InitEngine;

  ComboBox_init (ItemEx011,ItemEx012,ComboBoxEx1);  // ALLCALL ON/OFF
  ComboBox_init (ItemEx021,ItemEx022,ComboBoxEx2);  // SUB3 ON/OFF
  ComboBox_init (ItemEx031,ItemEx032,ComboBoxEx3);  // SUB2 ON/OFF
  ComboBox_init (ItemEx041,ItemEx042,ComboBoxEx4);  // SUB1 ON/OFF
  ComboBox_init (ItemEx051,ItemEx052,ComboBoxEx5);  // SLEEP ON/OFF

  ComboBox_init (ItemEx061,ItemEx062,ComboBoxEx6);  // OUTDRV ON/OFF
  ComboBox_init (ItemEx071,ItemEx072,ComboBoxEx7);  // OCH ON/OFF
  ComboBox_init (ItemEx081,ItemEx082,ComboBoxEx8);  // INVRT ON/OFF
  ComboBox_init (ItemEx091,ItemEx092,ComboBoxEx9);  // DMBLNK ON/OFF

  ComboBox_init (ItemEx101,ItemEx102,ComboBoxEx10); // LDR0 ON/OFF
  ComboBox_init (ItemEx111,ItemEx112,ComboBoxEx11); // LDR1 ON/OFF
  ComboBox_init (ItemEx121,ItemEx122,ComboBoxEx12); // LDR2 ON/OFF
  ComboBox_init (ItemEx131,ItemEx132,ComboBoxEx13); // LDR3 ON/OFF

  Py_S := TStringList.Create;
  Py_S.Delimiter := '|';
  Py_S.StrictDelimiter := True;
  Py_S.DelimitedText := 'from  i2c_pkg.pca9632_pkg import pca9632_driver|' +
                        'reg_view = pca9632_driver.read_pca9632()|' +
                        'print ("{}".format(reg_view))|';

  PythonEngine1.ExecStrings(Py_S);
  Py_S.Free;

end;

procedure TForm1.RadioButton1Change(Sender: TObject);
begin

end;

procedure TForm1.Edit1Click(Sender: TObject);
begin
  Edit1.ReadOnly:=false;
  Edit1.Color:=clWhite;
end;

procedure TForm1.Edit2Click(Sender: TObject);
begin
  Edit2.ReadOnly:=false;
  Edit2.Color:=clWhite;
end;

end.

