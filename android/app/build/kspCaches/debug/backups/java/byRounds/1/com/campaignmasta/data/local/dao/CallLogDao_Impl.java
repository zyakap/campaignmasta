package com.campaignmasta.data.local.dao;

import android.database.Cursor;
import android.os.CancellationSignal;
import androidx.annotation.NonNull;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.SharedSQLiteStatement;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.campaignmasta.data.local.entity.CallLogEntity;
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
public final class CallLogDao_Impl implements CallLogDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<CallLogEntity> __insertionAdapterOfCallLogEntity;

  private final SharedSQLiteStatement __preparedStmtOfMarkSynced;

  private final SharedSQLiteStatement __preparedStmtOfMarkFailed;

  public CallLogDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfCallLogEntity = new EntityInsertionAdapter<CallLogEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `call_logs` (`localId`,`serverId`,`personCalled`,`personType`,`phoneNumber`,`callDatetime`,`callOutcome`,`discussionSummary`,`issuesRaised`,`commitmentsMade`,`followUpRequired`,`followUpDate`,`influencerId`,`supporterId`,`callerId`,`updatedAt`,`syncStatus`,`createdLocallyAt`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final CallLogEntity entity) {
        statement.bindString(1, entity.getLocalId());
        if (entity.getServerId() == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.getServerId());
        }
        statement.bindString(3, entity.getPersonCalled());
        statement.bindString(4, entity.getPersonType());
        statement.bindString(5, entity.getPhoneNumber());
        statement.bindString(6, entity.getCallDatetime());
        statement.bindString(7, entity.getCallOutcome());
        statement.bindString(8, entity.getDiscussionSummary());
        statement.bindString(9, entity.getIssuesRaised());
        statement.bindString(10, entity.getCommitmentsMade());
        final int _tmp = entity.getFollowUpRequired() ? 1 : 0;
        statement.bindLong(11, _tmp);
        if (entity.getFollowUpDate() == null) {
          statement.bindNull(12);
        } else {
          statement.bindString(12, entity.getFollowUpDate());
        }
        if (entity.getInfluencerId() == null) {
          statement.bindNull(13);
        } else {
          statement.bindLong(13, entity.getInfluencerId());
        }
        if (entity.getSupporterId() == null) {
          statement.bindNull(14);
        } else {
          statement.bindLong(14, entity.getSupporterId());
        }
        if (entity.getCallerId() == null) {
          statement.bindNull(15);
        } else {
          statement.bindLong(15, entity.getCallerId());
        }
        statement.bindString(16, entity.getUpdatedAt());
        statement.bindString(17, entity.getSyncStatus());
        statement.bindLong(18, entity.getCreatedLocallyAt());
      }
    };
    this.__preparedStmtOfMarkSynced = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE call_logs SET serverId = ?, syncStatus = 'SYNCED' WHERE localId = ?";
        return _query;
      }
    };
    this.__preparedStmtOfMarkFailed = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE call_logs SET syncStatus = 'FAILED' WHERE localId = ?";
        return _query;
      }
    };
  }

  @Override
  public Object insert(final CallLogEntity entity, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfCallLogEntity.insert(entity);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object markSynced(final String localId, final int serverId,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfMarkSynced.acquire();
        int _argIndex = 1;
        _stmt.bindLong(_argIndex, serverId);
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
          __preparedStmtOfMarkSynced.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Object markFailed(final String localId, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfMarkFailed.acquire();
        int _argIndex = 1;
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
          __preparedStmtOfMarkFailed.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<CallLogEntity>> getAllFlow() {
    final String _sql = "SELECT * FROM call_logs ORDER BY callDatetime DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"call_logs"}, new Callable<List<CallLogEntity>>() {
      @Override
      @NonNull
      public List<CallLogEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfPersonCalled = CursorUtil.getColumnIndexOrThrow(_cursor, "personCalled");
          final int _cursorIndexOfPersonType = CursorUtil.getColumnIndexOrThrow(_cursor, "personType");
          final int _cursorIndexOfPhoneNumber = CursorUtil.getColumnIndexOrThrow(_cursor, "phoneNumber");
          final int _cursorIndexOfCallDatetime = CursorUtil.getColumnIndexOrThrow(_cursor, "callDatetime");
          final int _cursorIndexOfCallOutcome = CursorUtil.getColumnIndexOrThrow(_cursor, "callOutcome");
          final int _cursorIndexOfDiscussionSummary = CursorUtil.getColumnIndexOrThrow(_cursor, "discussionSummary");
          final int _cursorIndexOfIssuesRaised = CursorUtil.getColumnIndexOrThrow(_cursor, "issuesRaised");
          final int _cursorIndexOfCommitmentsMade = CursorUtil.getColumnIndexOrThrow(_cursor, "commitmentsMade");
          final int _cursorIndexOfFollowUpRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpRequired");
          final int _cursorIndexOfFollowUpDate = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpDate");
          final int _cursorIndexOfInfluencerId = CursorUtil.getColumnIndexOrThrow(_cursor, "influencerId");
          final int _cursorIndexOfSupporterId = CursorUtil.getColumnIndexOrThrow(_cursor, "supporterId");
          final int _cursorIndexOfCallerId = CursorUtil.getColumnIndexOrThrow(_cursor, "callerId");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "syncStatus");
          final int _cursorIndexOfCreatedLocallyAt = CursorUtil.getColumnIndexOrThrow(_cursor, "createdLocallyAt");
          final List<CallLogEntity> _result = new ArrayList<CallLogEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final CallLogEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpPersonCalled;
            _tmpPersonCalled = _cursor.getString(_cursorIndexOfPersonCalled);
            final String _tmpPersonType;
            _tmpPersonType = _cursor.getString(_cursorIndexOfPersonType);
            final String _tmpPhoneNumber;
            _tmpPhoneNumber = _cursor.getString(_cursorIndexOfPhoneNumber);
            final String _tmpCallDatetime;
            _tmpCallDatetime = _cursor.getString(_cursorIndexOfCallDatetime);
            final String _tmpCallOutcome;
            _tmpCallOutcome = _cursor.getString(_cursorIndexOfCallOutcome);
            final String _tmpDiscussionSummary;
            _tmpDiscussionSummary = _cursor.getString(_cursorIndexOfDiscussionSummary);
            final String _tmpIssuesRaised;
            _tmpIssuesRaised = _cursor.getString(_cursorIndexOfIssuesRaised);
            final String _tmpCommitmentsMade;
            _tmpCommitmentsMade = _cursor.getString(_cursorIndexOfCommitmentsMade);
            final boolean _tmpFollowUpRequired;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfFollowUpRequired);
            _tmpFollowUpRequired = _tmp != 0;
            final String _tmpFollowUpDate;
            if (_cursor.isNull(_cursorIndexOfFollowUpDate)) {
              _tmpFollowUpDate = null;
            } else {
              _tmpFollowUpDate = _cursor.getString(_cursorIndexOfFollowUpDate);
            }
            final Integer _tmpInfluencerId;
            if (_cursor.isNull(_cursorIndexOfInfluencerId)) {
              _tmpInfluencerId = null;
            } else {
              _tmpInfluencerId = _cursor.getInt(_cursorIndexOfInfluencerId);
            }
            final Integer _tmpSupporterId;
            if (_cursor.isNull(_cursorIndexOfSupporterId)) {
              _tmpSupporterId = null;
            } else {
              _tmpSupporterId = _cursor.getInt(_cursorIndexOfSupporterId);
            }
            final Integer _tmpCallerId;
            if (_cursor.isNull(_cursorIndexOfCallerId)) {
              _tmpCallerId = null;
            } else {
              _tmpCallerId = _cursor.getInt(_cursorIndexOfCallerId);
            }
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpSyncStatus;
            _tmpSyncStatus = _cursor.getString(_cursorIndexOfSyncStatus);
            final long _tmpCreatedLocallyAt;
            _tmpCreatedLocallyAt = _cursor.getLong(_cursorIndexOfCreatedLocallyAt);
            _item = new CallLogEntity(_tmpLocalId,_tmpServerId,_tmpPersonCalled,_tmpPersonType,_tmpPhoneNumber,_tmpCallDatetime,_tmpCallOutcome,_tmpDiscussionSummary,_tmpIssuesRaised,_tmpCommitmentsMade,_tmpFollowUpRequired,_tmpFollowUpDate,_tmpInfluencerId,_tmpSupporterId,_tmpCallerId,_tmpUpdatedAt,_tmpSyncStatus,_tmpCreatedLocallyAt);
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
  public Object getPending(final Continuation<? super List<CallLogEntity>> $completion) {
    final String _sql = "SELECT * FROM call_logs WHERE syncStatus = 'PENDING' ORDER BY createdLocallyAt ASC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<List<CallLogEntity>>() {
      @Override
      @NonNull
      public List<CallLogEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfPersonCalled = CursorUtil.getColumnIndexOrThrow(_cursor, "personCalled");
          final int _cursorIndexOfPersonType = CursorUtil.getColumnIndexOrThrow(_cursor, "personType");
          final int _cursorIndexOfPhoneNumber = CursorUtil.getColumnIndexOrThrow(_cursor, "phoneNumber");
          final int _cursorIndexOfCallDatetime = CursorUtil.getColumnIndexOrThrow(_cursor, "callDatetime");
          final int _cursorIndexOfCallOutcome = CursorUtil.getColumnIndexOrThrow(_cursor, "callOutcome");
          final int _cursorIndexOfDiscussionSummary = CursorUtil.getColumnIndexOrThrow(_cursor, "discussionSummary");
          final int _cursorIndexOfIssuesRaised = CursorUtil.getColumnIndexOrThrow(_cursor, "issuesRaised");
          final int _cursorIndexOfCommitmentsMade = CursorUtil.getColumnIndexOrThrow(_cursor, "commitmentsMade");
          final int _cursorIndexOfFollowUpRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpRequired");
          final int _cursorIndexOfFollowUpDate = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpDate");
          final int _cursorIndexOfInfluencerId = CursorUtil.getColumnIndexOrThrow(_cursor, "influencerId");
          final int _cursorIndexOfSupporterId = CursorUtil.getColumnIndexOrThrow(_cursor, "supporterId");
          final int _cursorIndexOfCallerId = CursorUtil.getColumnIndexOrThrow(_cursor, "callerId");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "syncStatus");
          final int _cursorIndexOfCreatedLocallyAt = CursorUtil.getColumnIndexOrThrow(_cursor, "createdLocallyAt");
          final List<CallLogEntity> _result = new ArrayList<CallLogEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final CallLogEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpPersonCalled;
            _tmpPersonCalled = _cursor.getString(_cursorIndexOfPersonCalled);
            final String _tmpPersonType;
            _tmpPersonType = _cursor.getString(_cursorIndexOfPersonType);
            final String _tmpPhoneNumber;
            _tmpPhoneNumber = _cursor.getString(_cursorIndexOfPhoneNumber);
            final String _tmpCallDatetime;
            _tmpCallDatetime = _cursor.getString(_cursorIndexOfCallDatetime);
            final String _tmpCallOutcome;
            _tmpCallOutcome = _cursor.getString(_cursorIndexOfCallOutcome);
            final String _tmpDiscussionSummary;
            _tmpDiscussionSummary = _cursor.getString(_cursorIndexOfDiscussionSummary);
            final String _tmpIssuesRaised;
            _tmpIssuesRaised = _cursor.getString(_cursorIndexOfIssuesRaised);
            final String _tmpCommitmentsMade;
            _tmpCommitmentsMade = _cursor.getString(_cursorIndexOfCommitmentsMade);
            final boolean _tmpFollowUpRequired;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfFollowUpRequired);
            _tmpFollowUpRequired = _tmp != 0;
            final String _tmpFollowUpDate;
            if (_cursor.isNull(_cursorIndexOfFollowUpDate)) {
              _tmpFollowUpDate = null;
            } else {
              _tmpFollowUpDate = _cursor.getString(_cursorIndexOfFollowUpDate);
            }
            final Integer _tmpInfluencerId;
            if (_cursor.isNull(_cursorIndexOfInfluencerId)) {
              _tmpInfluencerId = null;
            } else {
              _tmpInfluencerId = _cursor.getInt(_cursorIndexOfInfluencerId);
            }
            final Integer _tmpSupporterId;
            if (_cursor.isNull(_cursorIndexOfSupporterId)) {
              _tmpSupporterId = null;
            } else {
              _tmpSupporterId = _cursor.getInt(_cursorIndexOfSupporterId);
            }
            final Integer _tmpCallerId;
            if (_cursor.isNull(_cursorIndexOfCallerId)) {
              _tmpCallerId = null;
            } else {
              _tmpCallerId = _cursor.getInt(_cursorIndexOfCallerId);
            }
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpSyncStatus;
            _tmpSyncStatus = _cursor.getString(_cursorIndexOfSyncStatus);
            final long _tmpCreatedLocallyAt;
            _tmpCreatedLocallyAt = _cursor.getLong(_cursorIndexOfCreatedLocallyAt);
            _item = new CallLogEntity(_tmpLocalId,_tmpServerId,_tmpPersonCalled,_tmpPersonType,_tmpPhoneNumber,_tmpCallDatetime,_tmpCallOutcome,_tmpDiscussionSummary,_tmpIssuesRaised,_tmpCommitmentsMade,_tmpFollowUpRequired,_tmpFollowUpDate,_tmpInfluencerId,_tmpSupporterId,_tmpCallerId,_tmpUpdatedAt,_tmpSyncStatus,_tmpCreatedLocallyAt);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @Override
  public Object count(final Continuation<? super Integer> $completion) {
    final String _sql = "SELECT COUNT(*) FROM call_logs";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<Integer>() {
      @Override
      @NonNull
      public Integer call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Integer _result;
          if (_cursor.moveToFirst()) {
            final int _tmp;
            _tmp = _cursor.getInt(0);
            _result = _tmp;
          } else {
            _result = 0;
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
