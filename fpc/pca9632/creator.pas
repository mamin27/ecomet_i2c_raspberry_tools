unit creator;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls;

type

  { TForm_creator }

  TForm_creator = class(TForm)
    Label_creator: TLabel;
    Label_project_name: TLabel;
    procedure FormCreate(Sender: TObject);
  private

  public

  end;

var
  Form_creator: TForm_creator;

implementation

{$R *.lfm}

{ TForm_creator }

procedure TForm_creator.FormCreate(Sender: TObject);
begin
  sleep(10000);
end;

end.

