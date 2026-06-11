package com.campaignmasta.data.local.dao;

import android.database.Cursor;
import android.os.CancellationSignal;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityDeletionOrUpdateAdapter;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.SharedSQLiteStatement;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.campaignmasta.data.local.entity.PollingLocationEntity;
import java.lang.Class;
import java.lang.Exception;
import java.lang.Integer;
import java.lang.Object;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class PollingLocationDao_Impl implements PollingLocationDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<PollingLocationEntity> __insertionAdapterOfPollingLocationEntity;

  private final EntityDeletionOrUpdateAdapter<PollingLocationEntity> __updateAdapterOfPollingLocationEntity;

  private final SharedSQLiteStatement __preparedStmtOfUpdateTally;

  private final SharedSQLiteStatement __preparedStmtOfDeleteAll;

  public PollingLocationDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfPollingLocationEntity = new EntityInsertionAdapter<PollingLocationEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `polling_locations` (`localId`,`serverId`,`name`,`wardName`,`wardId`,`gpsCoordinates`,`scrutineerName`,`scrutineerCheckedIn`,`securityRisk`,`expectedTurnout`,`status`,`notes`,`ourTally`,`updatedAt`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final PollingLocationEntity entity) {
        statement.bindString(1, entity.getLocalId());
        statement.bindLong(2, entity.getServerId());
        statement.bindString(3, entity.getName());
        statement.bindString(4, entity.getWardName());
        if (entity.getWardId() == null) {
          statement.bindNull(5);
        } else {
          statement.bindLong(5, entity.getWardId());
        }
        statement.bindString(6, entity.getGpsCoordinates());
        statement.bindString(7, entity.getScrutineerName());
        final int _tmp = entity.getScrutineerCheckedIn() ? 1 : 0;
        statement.bindLong(8, _tmp);
        statement.bindString(9, entity.getSecurityRisk());
        if (entity.getExpectedTurnout() == null) {
          statement.bindNull(10);
        } else {
          statement.bindLong(10, entity.getExpectedTurnout());
        }
        statement.bindString(11, entity.getStatus());
        statement.bindString(12, entity.getNotes());
        if (entity.getOurTally() == null) {
          statement.bindNull(13);
        } else {
          statement.bindLong(13, entity.getOurTally());
        }
        statement.bindString(14, entity.getUpdatedAt());
      }
    };
    this.__updateAdapterOfPollingLocationEntity = new EntityDeletionOrUpdateAdapter<PollingLocationEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "UPDATE OR ABORT `polling_locations` SET `localId` = ?,`serverId` = ?,`name` = ?,`wardName` = ?,`wardId` = ?,`gpsCoordinates` = ?,`scrutineerName` = ?,`scrutineerCheckedIn` = ?,`securityRisk` = ?,`expectedTurnout` = ?,`status` = ?,`notes` = ?,`ourTally` = ?,`updatedAt` = ? WHERE `localId` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final PollingLocationEntity entity) {
        statement.bindString(1, entity.getLocalId());
        statement.bindLong(2, entity.getServerId());
        statement.bindString(3, entity.getName());
        statement.bindString(4, entity.getWardName());
        if (entity.getWardId() == null) {
          statement.bindNull(5);
        } else {
          statement.bindLong(5, entity.getWardId());
        }
        statement.bindString(6, entity.getGpsCoordinates());
        statement.bindString(7, entity.getScrutineerName());
        final int _tmp = entity.getScrutineerCheckedIn() ? 1 : 0;
        statement.bindLong(8, _tmp);
        statement.bindString(9, entity.getSecurityRisk());
        if (entity.getExpectedTurnout() == null) {
          statement.bindNull(10);
        } else {
          statement.bindLong(10, entity.getExpectedTurnout());
        }
        statement.bindString(11, entity.getStatus());
        statement.bindString(12, entity.getNotes());
        if (entity.getOurTally() == null) {
          statement.bindNull(13);
        } else {
          statement.bindLong(13, entity.getOurTally());
        }
        statement.bindString(14, entity.getUpdatedAt());
        statement.bindString(15, entity.getLocalId());
      }
    };
    this.__preparedStmtOfUpdateTally = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE polling_locations SET ourTally = ? WHERE localId = ?";
        return _query;
      }
    };
    this.__preparedStmtOfDeleteAll = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "DELETE FROM polling_locations";
        return _query;
      }
    };
  }

  @Override
  public Object insertAll(final List<PollingLocationEntity> entities,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfPollingLocationEntity.insert(entities);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object update(final PollingLocationEntity entity,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __updateAdapterOfPollingLocationEntity.handle(entity);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object updateTally(final String localId, final int tally,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfUpdateTally.acquire();
        int _argIndex = 1;
        _stmt.bindLong(_argIndex, tally);
        _argIndex = 2;
        _stmt.bindString(_argIndex, localId);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfUpdateTally.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Object deleteAll(final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfDeleteAll.acquire();
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfDeleteAll.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<PollingLocationEntity>> getAllFlow() {
    final String _sql = "SELECT * FROM polling_locations ORDER BY name ASC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"polling_locations"}, new Callable<List<PollingLocationEntity>>() {
      @Override
      @NonNull
      public List<PollingLocationEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfName = CursorUtil.getColumnIndexOrThrow(_cursor, "name");
          final int _cursorIndexOfWardName = CursorUtil.getColumnIndexOrThrow(_cursor, "wardName");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfGpsCoordinates = CursorUtil.getColumnIndexOrThrow(_cursor, "gpsCoordinates");
          final int _cursorIndexOfScrutineerName = CursorUtil.getColumnIndexOrThrow(_cursor, "scrutineerName");
          final int _cursorIndexOfScrutineerCheckedIn = CursorUtil.getColumnIndexOrThrow(_cursor, "scrutineerCheckedIn");
          final int _cursorIndexOfSecurityRisk = CursorUtil.getColumnIndexOrThrow(_cursor, "securityRisk");
          final int _cursorIndexOfExpectedTurnout = CursorUtil.getColumnIndexOrThrow(_cursor, "expectedTurnout");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfOurTally = CursorUtil.getColumnIndexOrThrow(_cursor, "ourTally");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final List<PollingLocationEntity> _result = new ArrayList<PollingLocationEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final PollingLocationEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final int _tmpServerId;
            _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            final String _tmpName;
            _tmpName = _cursor.getString(_cursorIndexOfName);
            final String _tmpWardName;
            _tmpWardName = _cursor.getString(_cursorIndexOfWardName);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final String _tmpGpsCoordinates;
            _tmpGpsCoordinates = _cursor.getString(_cursorIndexOfGpsCoordinates);
            final String _tmpScrutineerName;
            _tmpScrutineerName = _cursor.getString(_cursorIndexOfScrutineerName);
            final boolean _tmpScrutineerCheckedIn;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfScrutineerCheckedIn);
            _tmpScrutineerCheckedIn = _tmp != 0;
            final String _tmpSecurityRisk;
            _tmpSecurityRisk = _cursor.getString(_cursorIndexOfSecurityRisk);
            final Integer _tmpExpectedTurnout;
            if (_cursor.isNull(_cursorIndexOfExpectedTurnout)) {
              _tmpExpectedTurnout = null;
            } else {
              _tmpExpectedTurnout = _cursor.getInt(_cursorIndexOfExpectedTurnout);
            }
            final String _tmpStatus;
            _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final Integer _tmpOurTally;
            if (_cursor.isNull(_cursorIndexOfOurTally)) {
              _tmpOurTally = null;
            } else {
              _tmpOurTally = _cursor.getInt(_cursorIndexOfOurTally);
            }
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            _item = new PollingLocationEntity(_tmpLocalId,_tmpServerId,_tmpName,_tmpWardName,_tmpWardId,_tmpGpsCoordinates,_tmpScrutineerName,_tmpScrutineerCheckedIn,_tmpSecurityRisk,_tmpExpectedTurnout,_tmpStatus,_tmpNotes,_tmpOurTally,_tmpUpdatedAt);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Object getByLocalId(final String localId,
      final Continuation<? super PollingLocationEntity> $completion) {
    final String _sql = "SELECT * FROM polling_locations WHERE localId = ?";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindString(_argIndex, localId);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<PollingLocationEntity>() {
      @Override
      @Nullable
      public PollingLocationEntity call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfName = CursorUtil.getColumnIndexOrThrow(_cursor, "name");
          final int _cursorIndexOfWardName = CursorUtil.getColumnIndexOrThrow(_cursor, "wardName");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfGpsCoordinates = CursorUtil.getColumnIndexOrThrow(_cursor, "gpsCoordinates");
          final int _cursorIndexOfScrutineerName = CursorUtil.getColumnIndexOrThrow(_cursor, "scrutineerName");
          final int _cursorIndexOfScrutineerCheckedIn = CursorUtil.getColumnIndexOrThrow(_cursor, "scrutineerCheckedIn");
          final int _cursorIndexOfSecurityRisk = CursorUtil.getColumnIndexOrThrow(_cursor, "securityRisk");
          final int _cursorIndexOfExpectedTurnout = CursorUtil.getColumnIndexOrThrow(_cursor, "expectedTurnout");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfOurTally = CursorUtil.getColumnIndexOrThrow(_cursor, "ourTally");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final PollingLocationEntity _result;
          if (_cursor.moveToFirst()) {
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final int _tmpServerId;
            _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            final String _tmpName;
            _tmpName = _cursor.getString(_cursorIndexOfName);
            final String _tmpWardName;
            _tmpWardName = _cursor.getString(_cursorIndexOfWardName);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final String _tmpGpsCoordinates;
            _tmpGpsCoordinates = _cursor.getString(_cursorIndexOfGpsCoordinates);
            final String _tmpScrutineerName;
            _tmpScrutineerName = _cursor.getString(_cursorIndexOfScrutineerName);
            final boolean _tmpScrutineerCheckedIn;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfScrutineerCheckedIn);
            _tmpScrutineerCheckedIn = _tmp != 0;
            final String _tmpSecurityRisk;
            _tmpSecurityRisk = _cursor.getString(_cursorIndexOfSecurityRisk);
            final Integer _tmpExpectedTurnout;
            if (_cursor.isNull(_cursorIndexOfExpectedTurnout)) {
              _tmpExpectedTurnout = null;
            } else {
              _tmpExpectedTurnout = _cursor.getInt(_cursorIndexOfExpectedTurnout);
            }
            final String _tmpStatus;
            _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final Integer _tmpOurTally;
            if (_cursor.isNull(_cursorIndexOfOurTally)) {
              _tmpOurTally = null;
            } else {
              _tmpOurTally = _cursor.getInt(_cursorIndexOfOurTally);
            }
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            _result = new PollingLocationEntity(_tmpLocalId,_tmpServerId,_tmpName,_tmpWardName,_tmpWardId,_tmpGpsCoordinates,_tmpScrutineerName,_tmpScrutineerCheckedIn,_tmpSecurityRisk,_tmpExpectedTurnout,_tmpStatus,_tmpNotes,_tmpOurTally,_tmpUpdatedAt);
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
