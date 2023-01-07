from sqlalchemy.orm import Session

from src.crud.LedgerRepository import LedgerRepository
from src.dto.LedgerDto import RequestLedgerCreate, RequestLedgerUpdate
from src.entity.Model import UserLogin
from src.interface.Interface import AppService


class LedgerService(AppService):

    def create_ledger(self, ledger: RequestLedgerCreate, current_user: UserLogin):
        return LedgerRepository(self.db).create_ledger(ledger=ledger, current_user=current_user)

    def get_all_ledgers(self, current_user: UserLogin):
        return LedgerRepository(self.db).get_all_ledgers(current_user=current_user)

    def get_ledger(self, ledger_id: int, current_user: UserLogin):
        return LedgerRepository(self.db).get_ledger(ledger_id=ledger_id, current_user=current_user)

    def update_ledger(self, ledger_id: int,
                      updated_ledger: RequestLedgerUpdate, current_user: UserLogin):
        LedgerRepository(self.db).modify_ledger(ledger_id=ledger_id, updated_ledger=updated_ledger,
                                                current_user=current_user)

    def delete_leger(self, ledger_id: int, current_user: UserLogin):
        LedgerRepository(self.db).delete_ledger(ledger_id=ledger_id, current_user=current_user)
